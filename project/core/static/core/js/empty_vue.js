'use strict'

window.addEventListener('load', () => {
    let data_json = JSON.parse(document.getElementById('data_json').textContent)
    Vue.createApp({
        delimiters: ['[[', ']]'],

        data() {
            return {
            }
        },
        methods: {},
        mounted() {},
        computed: {},
        watch: {}
    }).mount('#app')
})
