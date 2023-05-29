<template>
    <div id="signup">
        <v-row class="mt-10" no-gutters>
            <v-col class="mx-auto" cols="12" sm="4">
                <v-card>
                    <div class="text-h5 ml-5 mt-5">Sign up</div>

                    <form ref="form" class="pa-5" @submit.prevent="signUp">
                        <v-text-field
                                v-model="username"
                                :rules="rules"
                                label="username"
                        ></v-text-field>

                        <v-text-field
                                v-model="email"
                                :rules="rulesEmail"
                                label="email"
                        ></v-text-field>

                        <v-text-field
                                v-model="password"
                                :rules="rules"
                                label="password"
                                type="password"
                        ></v-text-field>

                        <v-col class="text-right mt-6 pa-0">
                            <v-btn :disabled="!!loadingProcess" class="mr-3" color="orange-darken-3" size="small"
                                   type="submit">sigh up
                            </v-btn>

                            <v-btn class="mr-3" size="small" to="/">
                                return to login
                            </v-btn>
                        </v-col>

                    </form>
                    <div class="text-center">{{ textResult }}</div>
                </v-card>
            </v-col>
        </v-row>

    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "signup",
    components: {},
    data() {
        return {
            username: null,
            email: null,
            password: null,
            loadingProcess: false,
            textResult: '',
            rules: [
                v => !!v || 'required field',
            ],
            rulesEmail: [
                v => !!v || 'required field',
                v => /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'invalid email'
            ],
        }
    },
    methods: {
        validateAllRequiredFields: function (dataValue) {
            return Object.values(dataValue).every((val) => {
                return !!val
            })
        },
        signUp: function () {
            let body = {
                "username": this.username,
                "email": this.email,
                "password": this.password,
            }

            if (this.validateAllRequiredFields(body)) {
                this.loadingProcess = true
                this.textResult = ''
                axios.post('api/user/signup/', body, {headers:{ Authorization:""}})
                    .then(response => {
                        if (response.status === 201) {
                            this.textResult = 'User was created. You can log in.';
                        }
                        this.$refs.form.reset()
                        this.loadingProcess = false
                    })
                    .catch(error => {
                        this.loadingProcess = false
                        this.textResult = error.response.data
                    });
            } else {
                this.textResult = 'Fill all fields';
            }
        },

    },
}
</script>