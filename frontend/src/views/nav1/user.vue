<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-input v-model="filters.name" placeholder="姓名"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="getUser">查询</el-button>
				</el-form-item>
			</el-form>
		</el-col>

		<!--列表-->
		<template>
			<el-table :data="users" highlight-current-row v-loading="loading" style="width: 100%;">
				<el-table-column type="index" width="120">
				</el-table-column>
				<el-table-column prop="username" label="用户名" sortable>
				</el-table-column>
				<el-table-column prop="password" label="密码" sortable>
				</el-table-column>
				<el-table-column prop="platform" label="平台名" sortable>
				</el-table-column>
			</el-table>
		</template>
	</section>
</template>
<script>
	import { getUserList } from '../../api/api';
	export default {
		data() {
			return {
				filters: {
					name: ''
				},
				loading: false,
				users: [
				]
			}
		},
		methods: {
			//获取用户列表
			getUser: function () {
				let para = {
					page: 1,
					pageSize: 20
				};
				this.loading = true;
				getUserList(para).then((res) => {
					this.users = res.data.data;
					console.log(this.users);
					this.loading = false;
				});
			}
		},
		mounted() {
//			this.getUser();
		}
	};

</script>

<style scoped>

</style>