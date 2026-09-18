import random
import time

def guess_number_game():
    # 1. 生成一个 1 到 100 之间的随机整数
    target_number = random.randint(1, 100)
    attempts = 0
    
    print("=" * 30)
    print("欢迎来到猜数字小游戏！")
    print("我已经想好了一个 1 到 100 之间的数字。")
    print("=" * 30)

    while True:
        try:
            # 2. 获取用户输入并转换为整数
            user_input = input("\n请输入你猜的数字: ")
            guess = int(user_input)
            attempts += 1

            # 3. 判断猜测结果
            if guess < target_number:
                print("猜小了！再大一点。")
            elif guess > target_number:
                print("猜大了！再小一点。")
            else:
                # 猜对了，结束循环
                print(f"\n🎉 恭喜你！猜对了！答案就是 {target_number}。")
                print(f"你总共猜了 {attempts} 次。")
                break
                
        except ValueError:
            # 处理输入非数字的情况
            print("⚠️ 输入无效，请输入一个整数！")

    # 4. 简单的倒计时结束程序
    print("\n游戏将在 3 秒后自动关闭...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("再见！")

if __name__ == "__main__":
    guess_number_game()