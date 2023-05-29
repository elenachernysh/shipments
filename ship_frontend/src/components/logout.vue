<template>
    <div id="logout" style="margin-left: 15px;">
        <v-btn @click="logout">
            log out
        </v-btn>
    </div>
</template>

<script>
export default {
    name: "logout",
    methods: {
        logout: function () {
            this.$store.dispatch("deleteAuthTokens")
            this.$router.push({name: "login"})
        }
    },
}
</script>
