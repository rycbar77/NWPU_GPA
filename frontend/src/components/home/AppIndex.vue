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
            <el-descriptions-item label="已修学分">{{ creditSum }}</el-descriptions-item>

          </el-descriptions>
        </el-card>
        <div v-for="index in tableData.length" :key="index">
          <el-card>
            <el-container>
              <el-tag effect="plain">
                {{ tableData[index - 1][Object.keys(tableData[index - 1])[0]]["semester"] }}
              </el-tag>
              <el-col :span="18"></el-col>

              <el-tag effect="light">
                学分绩：{{ semesterAverage[index - 1].toFixed(2) }}
              </el-tag>
            </el-container>
            <!--              <el-col :span="15"></el-col>-->
            <!--              <el-col :push="1">-->
            <!--                <el-switch-->
            <!--                    v-model="semester_statuses[index-1]"-->
            <!--                    :active-value="1"-->
            <!--                    :inactive-value="0"-->
            <!--                    active-color="#13ce66"-->
            <!--                    inactive-color="#ff4949"-->
            <!--                    @change="changeSwitchAll(index-1)"/>-->
            <!--              </el-col>-->
            <!--            </el-container>-->
            <el-table
                ref="multiTable"
                :data="tableData[index-1]"
                stripe
                height="400"
                @selection-change="(selections)=>{handleSelection(selections,index-1)}">
              <el-table-column
                  type="selection"
                  width="55">
              </el-table-column>
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
              <!--              <el-table-column-->
              <!--                  label="选择"-->
              <!--              >-->
              <!--                <template slot-scope="scope">-->
              <!--                  <el-switch-->
              <!--                      v-model="scope.row.status"-->
              <!--                      :active-value="1"-->
              <!--                      :inactive-value="0"-->
              <!--                      active-color="#13ce66"-->
              <!--                      inactive-color="#ff4949"-->
              <!--                      @change="changeSwitch(scope.row)"/>-->
              <!--                </template>-->
              <!--              </el-table-column>-->
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
      semesterCreditSum: [],
      semesterScoreSum: [],
      semesterAverage: [],
      refs:[]
    }
  },
  methods: {
    parse_course() {
      let table = []
      let semester_name = ""
      let tmp_semester_name = ""
      let semester_table = []
      let tmp_score_sum = 0
      let tmp_credit_sum = 0
      // console.log(this.$route.params)
      // console.log(this.courses[0])
      for (const id in this.courses) {
        // console.log(id)
        let tmp = this.courses[id]
        // console.log(tmp["name"])
        semester_name = tmp["semester"]
        if (semester_name !== tmp_semester_name && tmp_semester_name !== "") {
          table.push(semester_table)
          this.semesterScoreSum.push(tmp_score_sum)
          this.semesterCreditSum.push(tmp_credit_sum)
          this.semesterAverage.push(tmp_score_sum / tmp_credit_sum)
          this.scoreSum += tmp_score_sum
          this.creditSum += tmp_credit_sum
          tmp_score_sum = 0
          tmp_credit_sum = 0
          semester_table = []
        }
        tmp_semester_name = semester_name
        let total = tmp["score"]["total"]
        tmp["score"]["total"] = Number(total) ? Number(total) : total
        // tmp['status'] = Number(total) && Number(tmp["credit"]) !== 0 ? 1 : 0
        tmp_credit_sum += Number(total) ? Number(tmp["credit"]) : 0
        tmp_score_sum += Number(total) ? Number(total) * Number(tmp["credit"]) : 0
        semester_table.push(tmp)
      }
      table.push(semester_table)
      this.semesterScoreSum.push(tmp_score_sum)
      this.semesterCreditSum.push(tmp_credit_sum)
      this.semesterAverage.push(tmp_score_sum / tmp_credit_sum)
      this.scoreSum += tmp_score_sum
      this.creditSum += tmp_credit_sum
      tmp_score_sum = 0
      tmp_credit_sum = 0
      semester_table = []
      // console.log(table)
      this.average = this.scoreSum / this.creditSum
      this.tableData = table
    },
    goBack() {
      this.$router.push({path: '/'})
    },
    handleSelection(selections, index) {
      this.scoreSum -= this.semesterScoreSum[index]
      this.creditSum -= this.semesterCreditSum[index]
      this.calSemesterGPA(selections, index)
      this.scoreSum += this.semesterScoreSum[index]
      this.creditSum += this.semesterCreditSum[index]
      this.average = this.scoreSum / this.creditSum
      // if (Number(row["score"]["total"])) {
      //   if (row["status"]) {
      //     this.creditSum += Number(row["credit"])
      //     this.scoreSum += Number(row["credit"]) * row["score"]["total"]
      //     this.average = this.scoreSum / this.creditSum
      //   } else {
      //     this.creditSum -= Number(row["credit"])
      //     this.scoreSum -= Number(row["credit"]) * row["score"]["total"]
      //     this.average = this.scoreSum / this.creditSum
      //   }
      // }
      // console.log(selections, index)
    },
    calSemesterGPA(table, index) {
      let scoreSum = 0
      let creditSum = 0
      for (let i = 0; i < table.length; i++) {
        let course = table[i];
        let total = course["score"]["total"]
        creditSum += Number(total) ? Number(course["credit"]) : 0
        scoreSum += Number(total) ? Number(total) * Number(course["credit"]) : 0
      }

      this.semesterScoreSum[index] = scoreSum
      this.semesterCreditSum[index] = creditSum
      this.semesterAverage[index] = scoreSum / creditSum
    },
    // changeSwitchAll(index) {
    //   let table = this.tableData[index]
    //
    //   for (let j = 0, len = table.length; j < len; j++) {
    //     table[j]["status"] = this.semester_statuses[index]
    //   }
    // console.log(index)
    // }
  },
  mounted() {
    this.parse_course();
    this.$nextTick(() => {
      let tables=this.$refs.multiTable
      for(let i=0;i<tables.length;i++)
      {
        // console.log(tables[i])
        tables[i].toggleAllSelection()
      }
    })
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
  width: 850px;
  margin: 0 auto;
}
</style>