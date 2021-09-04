<template>
  <el-container>

    <el-header>
      <el-card>
        <el-page-header @back="goBack" content="详情页面">
        </el-page-header>
      </el-card>


    </el-header>
    <el-main>
      <div class="frame">
        <el-card>
          <el-descriptions title="信息">
            <el-descriptions-item label="学号">{{ this.$store.state.user.username }}</el-descriptions-item>
            <el-descriptions-item label="学分绩">{{ average.toFixed(2) }}</el-descriptions-item>

          </el-descriptions>
        </el-card>
        <div v-for="index in tableData.length" :key="index">
          <el-card>
            <el-container>
              <el-tag effect="plain">
                {{ tableData[index - 1][Object.keys(tableData[index - 1])[0]]["semester"] }}
              </el-tag>
              <el-col :span="15"></el-col>
              <el-col :push="1">
                <el-switch
                    v-model="semester_statuses[index-1]"
                    :active-value="1"
                    :inactive-value="0"
                    active-color="#13ce66"
                    inactive-color="#ff4949"
                    @change="changeSwitchAll(index-1)"/>
              </el-col>
            </el-container>
            <el-table
                :data="test"
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
        </div>
      </div>
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
      average: 0,
      semester_statuses: [],
      course_statuses: [],
      test: []
    }
  },
  methods: {
    parse_course() {
      let table = []
      let semester_name = ""
      let tmp_semester_name = ""
      let semester_table = []
      let tmp_status = 1
      for (const id in this.courses) {
        let tmp = this.courses[id]
        semester_name = tmp["semester"]
        // console.log(semester_name)
        if (semester_name !== tmp_semester_name && tmp_semester_name !== "") {
          // console.log(semester_table)
          table.push(semester_table)
          this.semester_statuses.push(tmp_status)
          semester_table = []
        }
        tmp_semester_name = semester_name
        let total = tmp["score"]["total"]
        // console.log(Number(total))
        tmp["score"]["total"] = Number(total) ? Number(total) : total
        tmp['status'] = Number(total) && Number(tmp["credit"]) !== 0 ? 1 : 0
        // this.course_statuses.push(Number(total) && Number(tmp["credit"]) !== 0 ? 1 : 0)
        if (!tmp["status"]) {
          tmp_status = 0
        }
        this.creditSum += Number(total) ? Number(tmp["credit"]) : 0
        this.scoreSum += Number(total) ? Number(total) * Number(tmp["credit"]) : 0
        semester_table.push(tmp)
      }
      table.push(semester_table)
      semester_table = []
      this.semester_statuses.push(tmp_status)
      // console.log(this.scoreSum)
      // console.log(this.creditSum)
      this.average = this.scoreSum / this.creditSum
      // console.log(table)
      this.tableData = table
      this.test = table[0]
      // console.log(this.test)
    },
    goBack() {
      this.$router.push({path: '/'})
    },
    changeSwitch(row) {
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

    },
    changeSwitchAll(index) {
      let table = this.tableData[index]

      for (let j = 0, len = table.length; j < len; j++) {
        table[j]["status"] = this.semester_statuses[index]
      }
      // console.log(index)
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

.el-row {
  margin-bottom: 10px;
}

.el-col {
  margin-bottom: 10px;
  margin-right: 8px;
  margin-left: 8px;
}

.frame {
  width: 900px;
  margin: 0 auto;
}
</style>