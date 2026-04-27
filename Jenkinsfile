node {
    stage('Build') {
        echo 'Hello from Jenkins!'
    }
}

pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

	
        stage('Run Tests') {
            steps {
 		// 全局安装 Midscene CLI
       		 sh 'npm install -g @midscene/cli'
                // 👇 执行的命令请替换为你项目中实际的测试命令
                sh 'npx midscene ./SeleniumTest/test_login.yaml'
                // 或使用其他方式生成报告，确保报告被输出到了指定路径
            }
        }
 }

    post {
        always {
            // 👇 发布 Midscene 生成的 HTML 报告
            publishHTML(
                target: [
                    allowMissing: false,              // 如果报告缺失，是否将构建标记为失败
                    alwaysLinkToLastBuild: false,    // 是否总是链接到最后一次构建的报告
                    keepAll: true,                   // 是否保留所有历史报告
                    reportDir: 'midscene_run/report', // 报告所在的目录（相对于工作区）
                    reportFiles: 'test_login.html',       // 报告的入口文件名
                    reportName: 'Midscene Test Report' // 报告在 Jenkins 侧边栏显示的名称
                ]
            )
        }
    }
}