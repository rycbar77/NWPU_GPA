<template>
  <body id="poster">
  <el-form class="login-container" label-position="left"
           label-width="0px">
    <h3 class="login_title">系统登录</h3>
    <el-form-item>
      <el-input type="text" v-model="loginForm.username"
                auto-complete="off" placeholder="学号"></el-input>
    </el-form-item>
    <el-form-item>
      <el-input type="password"  v-model="loginForm.password"
                auto-complete="off" placeholder="密码"></el-input>
    </el-form-item>
    <el-form-item style="width: 100%">
      <el-button  style="width: 30%" @click="login" round>注册</el-button>
      <el-button type="primary" style="width: 30%;background: #505458;border: none" @click="login" round>登录</el-button>
    </el-form-item>
  </el-form>

  <el-dialog  title="提示"
              :visible.sync="dialogVisible"
              :modal=false
              :close-on-press-escape=false
              :close-on-click-modal=false
              width="30%">
    <span>学号或密码错误</span>
    <span slot="footer" class="dialog-footer">
    <!-- <el-button @click="dialogVisible = false">取 消</el-button> -->
    <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
  </span>
  </el-dialog>
  </body>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      responseResult: [],
      dialogVisible: false
    }
  },
  methods: {
    login () {
      const _this = this;
      console.log(_this.$store.state)
      this.$axios
          .post('/', {
            username: this.loginForm.username,
            password: this.loginForm.password
          })
          .then((successResponse) => {
            if (successResponse.data.code === 200) {
              _this.$store.commit('login', _this.loginForm)
              var path = this.$route.query.redirect
              this.$router.replace({path: path === '/' || path === undefined ? '/index' : path})
            } else if (successResponse.data.code === 400) {
              _this.dialogVisible = true
              console.log(_this.dialogVisible)
            }
          })
          .catch(() => { })
    }
  }
}
</script>

<style>
#poster {
  background:url("../assets/rick&morty.jpg") no-repeat;
  background-position: center;
  height: 100%;
  width: 100%;
  background-size: cover;
  position: fixed;
}
body{
  margin: 0px;
}
.login-container {
  border-radius: 15px;
  background-clip: padding-box;
  margin: 90px auto;
  width: 350px;
  padding: 35px 35px 15px 35px;
  background: #fff;
  border: 1px solid #eaeaea;
  box-shadow: 0 0 25px #cac6c6;
}
.login_title {
  margin: 0px auto 40px auto;
  text-align: center;
  color: #505458;
}
</style>