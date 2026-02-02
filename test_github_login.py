import requests
from bs4 import BeautifulSoup

# GitHub 凭证信息
GITHUB_USERNAME = "s_d_001"
GITHUB_PASSWORD = "8463490hsb"

def test_github_login():
    """测试 GitHub 登录"""
    print("开始测试 GitHub 登录...")
    
    # 第一步：发送登录请求
    login_url = "https://github.com/session"
    session = requests.Session()
    
    # 获取登录页面（获取 authenticity_token）
    login_page = session.get("https://github.com/login")
    soup = BeautifulSoup(login_page.text, 'html.parser')
    
    # 提取 authenticity_token
    token_input = soup.find('input', {'name': 'authenticity_token'})
    if token_input:
        authenticity_token = token_input.get('value')
        print(f"✅ 获取到 authenticity_token: {authenticity_token[:20]}...")
    else:
        print("❌ 未能获取 authenticity_token")
        return None
    
    # 构造登录数据
    login_data = {
        'commit': 'Sign in',
        'authenticity_token': authenticity_token,
        'login': GITHUB_USERNAME,
        'password': GITHUB_PASSWORD,
        'webauthn-support': 'supported',
        'client_id': '',
        'return_to': ''
    }
    
    # 发送登录请求
    response = session.post(login_url, data=login_data, allow_redirects=False)
    
    print(f"响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ 登录请求发送成功")
        
        # 检查是否有 2FA 要求
        if response.text.find('two-factor') != -1:
            print("⚠️ 需要两步验证")
            return None
        
        # 检查是否登录成功
        if 'session' in session.cookies:
            print("✅ 登录成功！")
            return session
        else:
            print("❌ 登录失败，可能是密码错误或需要验证")
            return None
    else:
        print(f"❌ 登录请求失败，状态码: {response.status_code}")
        return None

if __name__ == '__main__':
    test_github_login()
