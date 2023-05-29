import {createStore} from "vuex";

const store = createStore({
  state () {
    return {
      accessToken: null,
      refreshToken: null,
    }
  },
      getters: {
          getToken: (state) => {
              return state.accessToken
          },
      },
  mutations: {
    set_auth_tokens (state, {accessToken, refreshToken}) {
      state.accessToken = accessToken
      state.refreshToken = refreshToken
    },
    clearAuthTokens (state) {
              state.accessToken = null
      state.refreshToken = null
    }
  },
  actions: {
    set_auth_tokens ({ commit }, accessToken, refreshToken) {
      commit('set_auth_tokens', accessToken, refreshToken);
    },
    deleteAuthTokens ({ commit }) {
        commit('clearAuthTokens')
    }
  }
})
export default store;