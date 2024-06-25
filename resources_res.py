import requests
from bs4 import BeautifulSoup
import pandas as pd


# 初始化数据列表
all_data = []

# 处理首页
home_url = 'http://xkz.mnr.gov.cn/ckxkz/index.html'
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}
response = requests.get(home_url, headers=headers)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

# 提取首页数据
rows = soup.select('.cent_three_box ul li')
for row in rows:
    cols = row.find_all('span')
    if len(cols) == 6:  # 确保每行有6个span元素
        entry = [col.text.strip() for col in cols]
        all_data.append(entry)

# 处理剩余页面
base_url = 'http://xkz.mnr.gov.cn/ckxkz/index_{}.html'
for i in range(1, 20):  # 从第2页到第20页
    url = base_url.format(i)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    # 提取数据
    rows = soup.select('.cent_three_box ul li')
    for row in rows:
        cols = row.find_all('span')
        if len(cols) == 6:  # 确保每行有6个span元素
            entry = [col.text.strip() for col in cols]
            all_data.append(entry)

# 创建DataFrame
columns = ['矿业权名称', '许可证号', '矿业权人', '矿种', '有效期起', '有效期止']
df = pd.DataFrame(all_data, columns=columns)

# 保存到Excel文件（.xlsx格式）
excel_file = 'mining_rights_data.xlsx'
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet1')

    # 自动调整列宽
    worksheet = writer.sheets['Sheet1']
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        worksheet.column_dimensions[column].width = adjusted_width

print(f"数据已保存到 {excel_file} 文件中")

# 显示DataFrame
# print(df)
