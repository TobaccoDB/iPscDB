const state = {
    showUser: false,
    showLogin: false
};
const getters = {
    isShow(state) {
        return state.showUser;
    },
    isLoginShow(state) {
        return state.showLogin
    }
}
const mutations = {
    hide(state) {
        state.showUser = false;
    },
    show(state) {
        state.showUser = true;
    },
    hideLogin(state) {
        state.showLogin = false;
    },
    showLogin(state) {
        state.showLogin = true;
    }
}
const actions = {
    showDailog({ commit }) {
        commit('show');
    },
    hideDailog({ commit }) {
        commit('hide');
    },
    showLoginDailog({ commit }) {
        commit('showLogin');
    },
    hideLoginDailog({ commit }) {
        commit('hideLogin');
    }
}
export default {
    namespaced: true,
    getters,
    mutations,
    actions,
    state
}