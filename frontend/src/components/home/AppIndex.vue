<template>
  <el-container>

    <el-header>
      <el-card>
        <el-page-header @back="goBack" content="详情页面">
        </el-page-header>
      </el-card>


    </el-header>
    <el-main>
      <el-card>
        <el-descriptions title="信息">
          <el-descriptions-item label="学号">{{ this.$store.state.user.username }}</el-descriptions-item>
          <el-descriptions-item label="学分绩">{{ average.toFixed(2) }}</el-descriptions-item>

        </el-descriptions>
      </el-card>
      <el-card>
        <el-table
            :data="tableData"
            stripe
            height="400"
        >
          <el-table-column
              prop="name"
              label="课程名"
          >
          </el-table-column>
          <el-table-column
              prop="credit"
              label="学分"
          >
          </el-table-column>
          <el-table-column
              prop="score.total"
              label="成绩"
          >
          </el-table-column>
          <el-table-column
              label="选择"
          >
            <template slot-scope="scope">
              <el-switch
                  v-model="scope.row.status"
                  :active-value="1"
                  :inactive-value="0"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                  @change="changeSwitch(scope.row)"/>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

    </el-main>
  </el-container>
  <!--    <div v-for="course in courses" :key="course.index">-->
  <!--      {{course["name"]}}    {{course["credit"]}}    {{course["score"]["total"]}}-->
  <!--    </div>-->


</template>

<script>
export default {
  name: 'AppIndex',
  data() {

    return {
      courses: this.$route.params,
      tableData: [],
      creditSum: 0,
      scoreSum: 0,
      average: 0
    }
  },
  methods: {
    parse_course() {
      let table = [];
      for (const id in this.courses) {
        let tmp = this.courses[id]
        let total = tmp["score"]["total"]
        // console.log(Number(total))
        tmp["score"]["total"] = Number(total) ? Number(total) : total
        tmp['status'] = Number(total) && Number(tmp["credit"]) !== 0 ? 1 : 0
        this.creditSum += Number(total) ? Number(tmp["credit"]) : 0
        this.scoreSum += Number(total) ? Number(total) * Number(tmp["credit"]) : 0
        table.push(tmp)
      }
      console.log(this.scoreSum)
      console.log(this.creditSum)
      this.average = this.scoreSum / this.creditSum
      // console.log(table)
      this.tableData = table
    },
    goBack() {
      this.$router.push({path: '/'})
    },
    changeSwitch(row) {
      // console.log(row);
      if (Number(row["score"]["total"])) {
        if (row["status"]) {
          this.creditSum += Number(row["credit"])
          this.scoreSum += Number(row["credit"]) * row["score"]["total"]
          this.average = this.scoreSum / this.creditSum
        } else {
          this.creditSum -= Number(row["credit"])
          this.scoreSum -= Number(row["credit"]) * row["score"]["total"]
          this.average = this.scoreSum / this.creditSum
        }
      }

    }
  },
  mounted() {
    this.parse_course();
  }
}


</script>

<style scoped>
.el-card {
  margin-bottom: 20px;
}
</style>