import sqlite3

def add_schedule(username):
    # 连接到数据库
    conn = sqlite3.connect('科创广场.db')
    cursor = conn.cursor()

    # 创建基础表（如果不存在）
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS `{username}` (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    ''')

    # 生成时间段列表
    time_slots = []
    for hour in range(0, 7):  # 0到6（含6）
        for minute in range(8, 23):  # 8到22（含22）
            time_slots.append(f"{hour}-{minute}")
    print("生成的时间段列表：", time_slots)

    # 获取现有列
    cursor.execute(f'PRAGMA table_info(`{username}`)')
    existing_columns = [col[1] for col in cursor.fetchall()]
    print("现有列：", existing_columns)

    # 动态添加字段
    for slot in time_slots:
        if slot not in existing_columns:
            cursor.execute(f'''
                ALTER TABLE `{username}` 
                ADD COLUMN `{slot}` TEXT DEFAULT '空闲'
            ''')
            print(f"已添加列：{slot}")

    # 更新现有数据
    for slot in time_slots:
        if slot in existing_columns:
            cursor.execute(f'''
                UPDATE `{username}`
                SET `{slot}` = '空闲'
                WHERE `{slot}` IS NULL OR `{slot}` = ''
            ''')
            print(f"已更新列：{slot}")

    # 插入一行空数据以触发默认值
    cursor.execute(f'''
        INSERT INTO `{username}` DEFAULT VALUES
    ''')

    # 提交更改并关闭连接
    conn.commit()
    conn.close()
    print("操作完成！")

def add_schedule_data(username, time, content):
    conn = sqlite3.connect('科创广场.db')
    cursor = conn.cursor()

    try:
        # 构建动态 SQL（用反引号包裹表名和字段名）
        query = f"UPDATE `{username}` SET `{time}` = ? WHERE id = 1"

        # 执行参数化查询（content 通过占位符传递）
        cursor.execute(query, (content,))
        conn.commit()

        # 可选：检查是否实际更新了数据
        if cursor.rowcount == 0:
            print("警告：未更新任何数据（可能不存在 id=1 的记录）")

    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
        conn.rollback()
    except Exception as e:
        print(f"错误: {e}")
    finally:
        conn.close()


def get_schedule_data(username):
    conn = sqlite3.connect('科创广场.db')
    cursor = conn.cursor()
    try:
        # 查询所有数据
        cursor.execute(f"SELECT * FROM `{username}`")
        rows = cursor.fetchall()
        print("查询结果：",rows)
        # 获取字段名列表（排除 id 字段）
        columns = [desc[0] for desc in cursor.description][1:]  # 去掉第一个字段 "id"

        # 构建键值对列表
        result = []
        for row in rows:
            # 将每行数据转为字典（id + 时间段字段）
            record = {"id": row[0]}  # 提取 id
            for col, value in zip(columns, row[1:]):  # 从第二列开始是时间段字段
                record[col] = value
            result.append(record)

        return result

    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
        return []
    finally:
        conn.close()
