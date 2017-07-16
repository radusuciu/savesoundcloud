Vue.use(VueResource);

var app = new Vue({
    el: '#app',
    data: {
        username: '',
        endpoint: 'likes'
    },
    computed: {
        downloadUrl: function() {
            return '/api/' + this.username + '/' + this.endpoint
        }
    },
    methods: {

    },
    mounted: function() {
        $('.ui.dropdown').dropdown();
    }
});
