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
                // 1. 如果存在错误的 package.json，先删除它
                sh 'rm -f package.json package-lock.json'

                // 2. 直接创建一个全新的、正确的 package.json
                sh '''
                    echo '{' > package.json
                    echo '  "name": "midscene-test",' >> package.json
                    echo '  "version": "1.0.0",' >> package.json
                    echo '  "description": "Jenkins Midscene tests",' >> package.json
                    echo '  "devDependencies": {' >> package.json
                    echo '    "@midscene/cli": "latest"' >> package.json
                    echo '  }' >> package.json
                    echo '}' >> package.json
                '''

                // 3. 验证 package.json 内容（可选）
                sh 'cat package.json'

                // 4. 清理可能损坏的 node_modules 并安装依赖
                sh 'rm -rf node_modules'
                sh 'npm install'
            }
        }

        stage('Run Tests') {
            steps {
                // 使用 npx 运行项目本地安装的 midscene 命令
                sh 'npx midscene ./test_login.yaml'
            }
        }
    }

    post {
        always {
            // 发布 Midscene 生成的 HTML 报告
            publishHTML(
                target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: false,
                    keepAll: true,
                    reportDir: 'midscene_run/report',
                    reportFiles: 'test_login.html',
                    reportName: 'Midscene Test Report'
                ]
            )
        }
    }
}