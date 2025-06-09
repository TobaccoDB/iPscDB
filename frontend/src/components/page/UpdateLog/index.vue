<template>
  <div class="UpdateLog">
    <div class="UpdateLog-inner" :style="{minHeight: contentHeight}" element-loading-text="loading" element-loading-background="#fff">
      <div>{{updateLogTitle}}</div>
      <div class="firstChild">{{updateLogTime}}</div>
      <!-- <div class="update-log-line"></div> -->
      <!-- <ul>
        <li v-for="item in updateLogData" :key="item.id">
          <span class="update-log-title">{{ item.title }}
          </span>
          <span class="update-log-time">{{ item.create_time | createTimeFilter }}</span>
        </li>
      </ul> -->
      <div class="updateLogContent">
        {{updateLogContent}}
      </div>
    </div>
  </div>
</template>
<script>
import { home_update_logs_detail } from "@/api/api";
export default {
  name: "UpdateLog",
  components: {
  },
  data() {
    return {
      contentHeight: (window.innerHeight - 330) + 'px',
      updateLogTitle: '',
      updateLogTime: '',
      updateLogContent: '',
    };
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      home_update_logs_detail(this.$route.query.id).then(res => {
        if (res.code == 200) {
          this.updateLogTitle = res.data.title
          this.updateLogTime = res.data.updated_at
          this.updateLogContent = res.data.content
        }
      });
    }
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>


