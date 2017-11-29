<template>
	<section>
		<!--工具条-->
		<el-row type="flex" class="toolbar" justify="space-between" style="padding-bottom: 0;">
			<el-col :span="6">
				<el-form :inline="true" :model="filters_spider" ref="filters_spider">
					<el-form-item>
						<el-input v-model="filters_spider.name" placeholder="爬虫ID或名称" style="width: 300px">
							<el-select v-model="filters_spider.select" slot="prepend" placeholder="请选择" style="width: 110px">
								<el-option label="任务ID" value="1"></el-option>
								<el-option label="任务名称" value="2"></el-option>
							</el-select>
						</el-input>
					</el-form-item>
					<el-form-item>
						<el-button type="primary" v-on:click="SearchByName">查询</el-button>
						<!--<el-button type="warning" v-on:click="resetForm('filters_spider')">重置</el-button>-->
					</el-form-item>
				</el-form>
			</el-col>
			<el-col :span="6">
				<div align="right">
					<el-button-group align="right">
						<el-button type="primary" @click="handleAdd">新增</el-button>
						<el-button type="primary" @click="refresh_data">刷新</el-button>
					</el-button-group>
				</div>
			</el-col>
		</el-row>


		<!--列表-->
		<el-table :data="spider" border highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<el-table-column type="selection">
			</el-table-column>
			<el-table-column prop="spider_id" label="爬虫任务ID" sortable>
			</el-table-column>
			<el-table-column prop="spider_createTime" label="爬虫创建时间" sortable>
                <template slot-scope="scope">
                    <el-icon name="time"></el-icon>
                    <span style="margin-left: 5px">{{ scope.row.spider_createTime }}</span>
                </template>
			</el-table-column>
			<el-table-column prop="spider_name" label="爬虫名称" sortable>
			</el-table-column>
			<el-table-column prop="spider_endTime" label="爬虫结束时间" sortable>
                <template slot-scope="scope">
                    <el-icon name="time"></el-icon>
                    <span style="margin-left: 5px">{{ scope.row.spider_endTime }}</span>
                </template>
			</el-table-column>
			<el-table-column prop="spider_status"
                             label="爬虫状态"
                             :filters="[{ text: '已完成', value: '已完成' }, { text: '正在爬取', value: '正在爬取' }, { text: '就绪', value: '就绪' }]"
                             :filter-method="filterTag"
                             filter-placement="bottom-end"
                             sortable>
			    <template slot-scope="scope">
                    <el-tag :type="scope.row.spider_status === '已完成' ? 'primary' : 'success'" close-transition>{{scope.row.spider_status}}</el-tag>
                </template>
            </el-table-column>
			<el-table-column prop="spider_currPage" label="爬虫当前页数" sortable>
			</el-table-column>
			<el-table-column prop="total_page" label="爬虫总页数" sortable>
			</el-table-column>
			<el-table-column prop="spider_all_items" label="爬虫总条数" sortable>
			</el-table-column>
            <el-table-column prop="spider_percent" label="爬虫进度" sortable>
                <template slot-scope="scope">
                    <el-progress :text-inside="true" :stroke-width="18" :percentage="scope.row.spider_percent"></el-progress>
                </template>
            </el-table-column>
			<el-table-column label="操作">
				<template slot-scope="scope">
					<el-button type="info" size="small" @click="handleEdit(spider.SpiderCode, scope.row)">编辑</el-button>
					<el-button type="danger" size="small" @click="handleDel(spider.SpiderCode, scope.row)">删除</el-button>
				</template>
			</el-table-column>
		</el-table>

		<!--工具条 1.分页-->
		<el-col :span="24" class="toolbar">
			<!--<el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>-->
			<el-pagination layout="total, prev, pager, next" @current-change="handleCurrentChange" :page-size="this.pageSize" :total="this.total" style="float:right;">
			</el-pagination>
		</el-col>

		<!--编辑界面-->
		<el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
			<el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
                <el-form-item label="爬虫任务ID" prop="spider_id">
                    <el-input v-model="editForm.spider_id" placeholder="点击右侧生成任务ID"></el-input>
                </el-form-item>
				<el-form-item label="爬虫名称" prop="spider_name">
					<el-input v-model="editForm.spider_name" auto-complete="off"></el-input>
				</el-form-item>
                <el-form-item label="爬虫运行状态" prop="spider_status">
                    <el-select v-model="editForm.spider_status" placeholder="请选择平台启动状态">
                        <el-option label="已完成" value="已完成"></el-option>
                        <el-option label="正在爬取" value="正在爬取"></el-option>
                        <el-option label="就绪" value="就绪"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="爬虫执行时间" prop="spider_createTime">
                    <el-date-picker
                            v-model="editForm.spider_createTime"
                            type="datetime"
                            placeholder="选择日期时间">
                    </el-date-picker>
                </el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button type="warning" @click.native="editFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="editSubmit" :loading="editLoading">状态更新</el-button>
				<el-button type="primary" :disabled="true">更新</el-button>
			</div>
		</el-dialog>

		<!--新增界面-->
		<el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
			<el-form :model="spiderForm" :rules="spiderFormRules" ref="spiderForm" label-width="100px" class="demo-spiderForm">
				<el-form-item label="爬虫任务ID" prop="spider_id" >
					<el-input v-model="spiderForm.spider_id" placeholder="点击右侧侧生成任务ID" ></el-input>
				</el-form-item>
				<el-form-item label="爬虫任务名称" prop="spider_name">
					<el-input v-model="spiderForm.spider_name" placeholder="请输入正确的任务名称"></el-input>
				</el-form-item>
				<el-form-item label="爬虫执行时间" prop="spider_createTime">
					<el-date-picker
							v-model="spiderForm.spider_createTime"
							type="datetime"
							placeholder="选择日期时间">
					</el-date-picker>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button type="primary" @click="submitIncrementSpider()">添加增量爬虫任务</el-button>
				<el-button @click="resetForm('spiderForm')">重置</el-button>
			</div>
		</el-dialog>

		<!-- 提示弹窗 -->
		<el-button plain @click="ErrorPopUp" v-show="false">错误</el-button>

	</section>
</template>

<script>
	import { getSpiderProcessInfo, editPlatformStatus, addPlatform } from '../../api/api';
    import ElInput from "../../../node_modules/element-ui/packages/input/src/input.vue";
    import ElButton from "../../../node_modules/element-ui/packages/button/src/button.vue";
    import ElCol from "element-ui/packages/col/src/col";
    import ElButtonGroup from "../../../node_modules/element-ui/packages/button/src/button-group.vue";
    import ElFormItem from "../../../node_modules/element-ui/packages/form/src/form-item.vue";
    import ElOption from "../../../node_modules/element-ui/packages/select/src/option.vue";

	export default {
        components: {
            ElOption,
            ElFormItem,
            ElButtonGroup,
            ElCol,
            ElButton,
            ElInput
		},
        data() {
			return {
			    //搜索功能
				filters_spider: {
				    name: '',
					select: ''
				},
				//搜索状态
				state: '',
				//爬虫列表
				spider: [],
				//初始化总页数，页码，每页个数
				total: 0,
				page: 1,
				pageSize: 10,
				//爬虫ID
                spider_id: '',
				//加载圈
				listLoading: false,
                //列表选中行
				sels: [],
                //编辑界面是否显示
				editFormVisible: false,
                //编辑界面载入
				editLoading: false,
                //编辑界面规则
                editFormRules: {
                    spider_id: [
                        { required: true, message: '请生成爬虫任务ID', trigger: 'blur' },
                    ],
                    spider_name: [
                        { required: true, message: '请输入爬虫名称', trigger: 'blur' },
                    ],
                    spider_status: [
                        { required: true, message: '请选择爬虫状态', trigger: 'blur' },
                    ],
				},
				//编辑界面数据
				editForm: {
                    spider_id: '',
                    spider_name: '',
                    spider_status: '',
                    spider_createTime: '',
				},
				addFormVisible: false,//新增界面是否显示
				addLoading: false,

				//任务提交界面数据
                spiderForm: {
                    spider_id: '',
                    spider_name: '',
                    //增量爬虫执行时间
                    spider_createTime: '',
                },

				//新增界面的表单规则
                spiderFormRules: {
                    spider_id: [
                        { required: true, message: '请输入爬虫ID', trigger: 'blur' }
                    ],
                    spider_name: [
                        { required: true, message: '请输入任务名称', trigger: 'blur' },
                        { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
                    ],
                },
			}
		},
		methods: {
			handleCurrentChange(val) {
				this.page = val;
				this.getSpiderProcessInfo();
			},
			//获取爬虫状态
			getSpiderProcessInfo() {
			  let para = {
			      sid: this.spider_id,
				  pn: this.page,
				  r: this.pageSize
			  };
			  this.listLoading = true;
			  getSpiderProcessInfo(para).then((res) => {
			      //总条数
			      this.total = res.count;
				  //数据
			      this.spider = res.data;

                  //时间戳转换标准日期
			      this.spider.forEach(function (val, index, arr) {
			          //闭包(转换时间)
                      function transferTime(value) {
                          let time = new Date(parseInt(value));
                          let Y = time.getFullYear() + '-';
                          let M = (time.getMonth() + 1 < 10 ? '0'+(time.getMonth()+1) : time.getMonth()+1) + '-';
                          let D = time.getDate()  + ' ';
                          let h = time.getHours() + ':';
                          let m = (time.getMinutes() < 10 ? '0' + (time.getMinutes()) : time.getMinutes()) + ':';
                          let s = (time.getSeconds() === 0 ? time.getSeconds() + '0': time.getSeconds()) ;
                          return Y + M + D + h + m + s;
                      }
                      //闭包(转换状态)
                      function transferSpiderStatus(value) {
                          let close = "已完成";
                          let running = "正在爬取";
                          let ready = "就绪";
                          if (value === "ClosedOrFinished"){
                              return close;
                          }else if (value === "Running"){
                              return running;
                          } else {
                              return ready;
						  }
                      }
                      //闭包(生成百分比)
                      function calculate_percent(value, total) {
                          return value / total * 100;
                      }
                      //转换创建时间和结束时间
                      arr[index].spider_createTime = transferTime(arr[index].spider_createTime);
                      arr[index].spider_endTime = transferTime(arr[index].spider_endTime);
                      //转换爬虫状态
                      arr[index].spider_status = transferSpiderStatus(arr[index].spider_status);

                      //新增一个字段
                      arr[index]['spider_percent'] = "";
                      //计算百分比
                      arr[index].spider_percent = calculate_percent(arr[index].spider_currPage, arr[index].total_page)
                  });
			      this.listLoading = false;
			  }).catch(error => {
                  if (error.response.status === 504){
                      this.listLoading = false;
                  }
              });
			},
			//刷新数据
            refresh_data() {
			    this.handleCurrentChange(1);
			},
			//查询数据
            SearchByName() {
			    let searchName = this.filters_spider.name;
			    let searchOption = this.filters_spider.select;
			    console.log("搜索选择: " + searchOption);
			    if (searchOption === ""){
                    this.$message({
                        message: '请选择你要搜索的条目!',
                        type: 'warning'
                    });
                } else {
                    if (typeof(searchName) === "undefined" || searchName === "") {
                        this.$message({
                            message: '你查询的是空值!请重新输入!',
                            type: 'warning'
                        });
                    }
                    else {
                        console.log("搜索的字段: " + this.filters_spider.name);
                        this.$message({
                            message: '暂时无法查询',
                            type: 'error'
                        });
                    }
                }

			},
			//删除
			handleDel: function (index, row) {
				this.$confirm('确认删除该记录吗?', '提示', {
					type: 'warning'
				}).then(() => {
					this.listLoading = true;
					let para = { id: row.id };
					this.$message({
						message: '暂时无法删除',
						type: 'error'
					});
					this.listLoading = false;
				}).catch(() => {

				});
			},
			//显示编辑界面
			handleEdit: function (index, row) {
				this.editFormVisible = true;
				this.editForm = Object.assign({}, row);
			},
			//显示新增界面
			handleAdd: function () {
				this.addFormVisible = true;
				this.spiderForm = {
                    spider_id: '',
                    spider_name: '',
                    spider_createTime: '',
				};
			},
            //提交增量爬虫
            submitIncrementSpider: function () {
				console.log(this.spiderForm);
            },
			//更新状态
//			editSubmit: function () {
//				this.$refs.editForm.validate((valid) => {
//				    let platformNewStatus = true;
//					if (valid) {
//						this.$confirm('确认提交吗？', '提示', {}).then(() => {
//							this.editLoading = true;
//							let platformName = this.editForm.platformName;
//							console.log("Status: " + this.editForm.platformStatus);
//                            if (this.editForm.platformStatus === '启用' ) {
//							  	platformNewStatus = true;
//							  	console.log("修改为true");
//							}
//							else if (this.editForm.platformStatus === '关闭' ) {
//                                platformNewStatus = false;
//                                console.log("修改为false");
//							}
//							console.log(platformNewStatus);
//							let para = { platformStatus: platformNewStatus, platformName: platformName };
//							para = window.JSON.stringify(para);
//							editPlatformStatus(para).then((res) => {
//								this.editLoading = false;
//								this.$message({
//									message: '更新成功',
//									type: 'success'
//								});
//								this.$refs['editForm'].resetFields();
//								this.editFormVisible = false;
//								this.getPlatform();
//							});
//						});
//					}
//				});
//			},
            //新增弹窗的重置按钮
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },
			//错误弹窗
            ErrorPopUp(errorMsg) {
                this.$notify.error({
                    title: '错误',
                    message: errorMsg
                });
            },
			CorrectPopUp(Msg){
                this.$notify({
                    title: '成功',
                    message: Msg,
                    type: 'success'
                });
			},
			selsChange: function (sels) {
				this.sels = sels;
			},
            filterTag(value, row) {
                return row.spider_status === value;
            },
			//批量删除
//			batchRemove: function () {
//				var ids = this.sels.map(item => item.id).toString();
//				this.$confirm('确认删除选中记录吗？', '提示', {
//					type: 'warning'
//				}).then(() => {
//					this.listLoading = true;
//					//NProgress.start();
//					let para = { ids: ids };
//					batchRemoveUser(para).then((res) => {
//						this.listLoading = false;
//						//NProgress.done();
//						this.$message({
//							message: '删除成功',
//							type: 'success'
//						});
//						this.getUsers();
//					});
//				}).catch(() => {
//
//				});
//			}
		},
		mounted() {
			this.getSpiderProcessInfo();
		}
	}

</script>

<style scope>

</style>