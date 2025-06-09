<template>
  <div class="cellIdentificationScope" :style="{ minHeight: '390px'}">
    <div style="height:100%;overflow: auto;" v-loading="loading">
      <iframe ref="benefitnotice_iframe" :src="iframeSrc" width="100%" height="100%" style="min-height:700px;" frameborder="0"></iframe>
    </div>
  </div>
</template>

<script>
export default {
  name: "cellIdentificationScope",
  components: {
  },
  data() {
    return {
      contentHeight: (window.innerHeight - 100 - 60 - 120) + 'px',
      loading: false,
      screenHeight: document.body.clientHeight,
      timer: false,
      iframeSrc: ''
    };
  },
  watch: {
    screenHeight(val) {
      // 为了避免频繁触发resize函数导致页面卡顿，使用定时器
      if (!this.timer) {
        // 一旦监听到的screenHeight值改变，就将其重新赋给data里的screenHeight
        this.contentHeight = (val - 100 - 60 - 120) + 'px'
        this.timer = true
        let that = this
        setTimeout(function () {
          that.timer = false
        }, 400)
      }
    },
  },
  mounted() {
    const that = this
    let firstFire = null;
    window.addEventListener('resize', () => {
      if (firstFire === null) {
        firstFire = setTimeout(function () {
          firstFire = null;
          return (() => {
            window.screenHeight = window.innerHeight
            that.screenHeight = window.screenHeight
          })()
        }, 100);
      }
    })

    this.init()
  },
  methods: {
    init() {
      this.loading = true;
      this.iframeSrc = 'http://159.138.151.49:55850/#/iPscDB/*/welcome/'
      const { benefitnotice_iframe } = this.$refs;
      // IE和非IE浏览器，监听iframe加载事件不一样，需要兼容
      const that = this;
      if (benefitnotice_iframe.attachEvent) {
        // IE
        benefitnotice_iframe.attachEvent('onload', () => {
          that.loading = false;
        });
      } else {
        // 非IE
        benefitnotice_iframe.onload = function () {
          that.loading = false;
        };
      }
    }
  }
};
</script>
<style lang="scss" scoped>
.cellIdentificationScope {
  width: 1240px;
  height: 100%;
  margin: 0 auto;
  padding: 30px 0;
}
</style>
