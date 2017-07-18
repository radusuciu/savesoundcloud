Vue.use(VueResource);

var app = new Vue({
    el: '#app',
    data: {
        username: '',
        endpoint: 'likes',
        bootstrap: {},
        errors: [],
        loading: false,
        uuid: null,
        interval: null
    },
    computed: {
        downloadUrl: function() {
            return this.username + '.zip?crumb=' + this.uuid;
        },
    },
    methods: {
        download: function(e) {
            // generate a new uuid right before request is started
            if (!this.username) {
                e.preventDefault();
                this.errors = ['Please enter a valid username'];
                return;
            }

            this.uuid = this.uuidv4();

            if (this.interval) {
                clearInterval(this.interval);
            }

            this.errors = [];
            this.loading = true;
            this.interval = setInterval(this.checkStatus(this.uuid), 1000);
        },
        checkStatus: function(uuid) {
            // using closure to make sure that we're not affected by uuid changes after the
            // request is started
            var uuid = uuid;
            var username = this.username;

            return function() {
                this.$http.get('/status/' + uuid).then(function(response) {
                    if (response.data !== 'started') {
                        clearInterval(this.interval);
                        this.loading = false;
                        this.errors = [];
                    }

                    if (response.data === 'error') {
                        this.userNotFound(username);
                    }
                });
            }.bind(this);
        },
        selectUser: function(username) {
            this.username = username;

            // clear errors because this would be triggered from autocomplete
            if (this.errors.length) {
                this.errors = [];
            }
        },
        userNotFound: function(username) {
            this.errors = ['User ' + username + ' not found.']
        },
        apiToAutocomplete: function(response) {
            return _.map(response, function(item) {
                return {
                    id: item.id,
                    title: item.permalink,
                    description: item.username,
                    image: item.avatar_url
                };
            });
        },
        uuidv4: function() {
            // https://stackoverflow.com/a/2117523/383744
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        }
    },
    mounted: function() {
        var me = this;

        this.bootstrap = window.bootstrap;

        this.$autocomplete = $('.ui.search').search({
            apiSettings: {
                url: '/api/find_user?term={query}',
                onResponse: function(response) {
                    return { results: me.apiToAutocomplete(response) }
                }
            },
            maxResults: 5,
            onSelect: function(item) {
                me.selectUser(item.title)
            }
        });
    },
    beforeDestroy: function() {
        clearInterval(this.interval);
    }
});
