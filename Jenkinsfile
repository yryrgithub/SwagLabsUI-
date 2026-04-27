pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // 项目本地安装 Midscene CLI（不需要全局权限）
                sh 'npm install'
            }
        }

        stage('Run Tests') {
            steps {
                // 使用 npx 运行项目本地的 midscene 命令
                sh 'npx midscene ./SeleniumTest/test_login.yaml'
            }
        }
    }

    post {
        always {
            // 发布 Midscene 生成的 HTML 报告
            publishHTML(
                target: [
                    allowMissing: true,               // 报告缺失时不导致构建失败
                    alwaysLinkToLastBuild: false,
                    keepAll: true,
                    reportDir: 'midscene_run/report', // Midscene 默认报告目录
                    reportFiles: 'index.html',        // 默认报告文件名
                    reportName: 'Midscene Test Report'
                ]
            )
        }
    }
}