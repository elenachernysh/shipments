<template>
    <div id="login" class="mt-10">
        <v-row no-gutters>
            <v-col class="mx-auto" cols="12" sm="4">
                <v-card class="pt-5" elevation="2">
                    <div class="text-h5 ml-5">Log in</div>

                    <form class="pa-5" @submit.prevent="login" @change="errMessage=''">
                        <v-text-field
                                v-model="username"
                                :rules="rules"
                                label="username"
                        ></v-text-field>

                        <v-text-field
                                v-model="password"
                                :rules="rules"
                                label="password"
                                type="password"
                        ></v-text-field>

                        <v-alert v-if="errMessage" border="top" color="orange-darken-3" dense type="error">
                            <p class="pa-0 ma-0 text-sm-body-2">{{ errMessage }}</p>
                        </v-alert>

                        <v-col class="text-right mt-6 pa-0">
                            <v-btn :disabled="!!loadingProcess" class="mr-3" color="orange-darken-3" size="small"
                                   type="submit">log in
                            </v-btn>

                            <v-btn class="mr-3" size="small" to="/signup">
                              sign up
                            </v-btn>
                        </v-col>
                    </form>
                </v-card>
            </v-col>
        </v-row>

    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "login",
    data() {
        return {
            password: null,
            username: null,
            rules: [
                v => !!v || 'required field',
                v => (v && v.length < 50) || 'must be less than 50 characters',
            ],
            errMessage: null,
            loadingProcess: false
        }
    },
    methods: {
        login: function () {
            if (!this.password || !this.username ) {
                this.errMessage = 'Both username or password are required.';
            }
            if (this.password && this.username) {
                let body = {
                    "username": this.username,
                    "password": this.password
                }
                axios.post('/api/user/token/', body)
                    .then(response => {
                        this.$store.dispatch('set_auth_tokens', {
                            accessToken: response.data['access'],
                            refreshToken: response.data['refresh']
                        });
                        this.loadingProcess = false;
                        this.$router.push({name: 'shipping'});
                    })
                    .catch(error => {
                        let errorResponse = error.toJSON()
                        if (errorResponse.status === 401) {
                            this.errMessage = 'You have entered an invalid username or password, or user does not exist. ';
                        } else {
                            this.errMessage = errorResponse.message;
                        }
                    })
            }
        },
    },
};
</script>
