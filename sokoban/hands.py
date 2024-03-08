# 导入所需的库
import cv2
import mediapipe as mp
import math

# 定义方向字典，用于存储食指的方向和对应的反馈信息
directions = {
    'up': "UP",
    'down': "DOWN",
    'left': "LEFT",
    'right': "RIGHT",
    'fist': 'FIST'
}

class Hands:
    def __init__(self):
        # 创建手部检测
        self.mp_hands = mp.solutions.hands
        #print('mphands',type(self.mp_hands))
        self.myhands = self.mp_hands.Hands(static_image_mode=False,\
                                           max_num_hands=2,min_detection_confidence=0.5,\
                                           min_tracking_confidence=0.5)
        #print('hands',type(self.hands))
        self.mp_drawing = mp.solutions.drawing_utils
        #print('mpdrawing',type(self.mp_drawing))
        # 设定重复帧 减少误差带来的影响
        self.init = 0
        self.direction_ = None
        self.direction_sent=None
        self.direction_sent_info=None
        self.image=None
        #视频帧数
        self.count=30

        self.cap=cv2.VideoCapture()


    # 只有当相同识别帧数到count帧时, 才会去显示对应的方向
    def counts(self,direction):
        # print(self.direction_)
        self.direction_sent=None
        if self.direction_ != direction:
            self.direction_ = direction
            self.init = 0
        elif self.direction_ == direction:
            self.init += 1
            # print(self.init)
            #为什么不用0-3，因为后面要用if判断

            if self.init >= self.count:
                # print(self.init)
                if self.direction_ == 'FIST':
                    self.direction_sent=5
                    self.direction_sent_info='fist'
                if self.direction_=='LEFT':
                    self.direction_sent=1
                    self.direction_sent_info = "left"
                elif self.direction_ =='RIGHT':
                    self.direction_sent=2
                    self.direction_sent_info = "right"
                elif self.direction_ =='UP':
                    self.direction_sent=3
                    self.direction_sent_info = "up"
                elif self.direction_ =='DOWN':
                    self.direction_sent=4
                    self.direction_sent_info = "down"
                self.init=0

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)

    def stop_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print('关闭摄像头')

    def run_camera(self):
        # print(self.cap.isOpened())
        if self.cap.isOpened():
            # print('enter loop')
            # 读取一帧图像并转换为RGB格式 cap摄像头
            success, image = self.cap.read()
            #             # print('image_raw',type(image))
            if not success:
                return
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # print('image_pro', type(image))

            # 将图像传入手部检测对象，并获取检测结果
            results = self.myhands.process(image)
            # print('results',type(results))
            # print('multihandlandmarks', type(results.multi_hand_landmarks))
            # print(results.multi_handedness)
            # 如果检测到至少一只手，则遍历每只手，并获取食指的方向和反馈信息
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # print(self.mp_hands.HandLandmark.INDEX_FINGER_MCP)
                    tip=[]
                    mcp=[]
                    for i in range(4,21,4):
                        tip1=hand_landmarks.landmark[i]
                        mcp1=hand_landmarks.landmark[i-3]
                        tip.append(tip1)
                        mcp.append(mcp1)
                    # print(x1,x2)
                    distance = ((tip[0].x - tip[1].x) ** 2 + (
                                tip[0].y - tip[1].y) ** 2) ** 0.5
                    angle=[]
                    for i in range(0,5):
                        if tip[i].x!=mcp[i].x:# 计算食指的斜率和角度（以度为单位）
                            # print('zhengchang')
                            slope = (tip[i].y - mcp[i].y) / (tip[i].x - mcp[i].x)
                        elif tip[i].y<=mcp[i].y:
                            slope = float('-inf')
                        else:
                            slope = float('inf')
                        angle1 = math.degrees(math.atan(slope))
                        angle.append(angle1)
                    # print(angle[1])
                    # 根据角度判断手势，并获取对应的反馈信息
                    if distance <0.05 and (angle[2] < -45 or angle[2] >45) and tip[3].y < mcp[3].y and (angle[3] < -45 or angle[3] >45) and tip[3].y < mcp[3].y:
                        direction = directions['fist']
                    elif (angle[0] < -45 or angle[0] >45) and tip[0].y < mcp[0].y:
                        direction = directions['up']

                    elif (angle[0] < -45 or angle[0] >45) and tip[0].y > mcp[0].y:
                        direction = directions['down']
                        #这里左右镜像了
                    elif (-45 < angle[0] < 45) and mcp[0].x > tip[0].x:
                        # print(angle[2],angle[3],angle[4])
                        direction = directions['right']
                    else:
                        direction = directions['left']
                    # print(direction)
                    self.counts(direction)
                    if self.direction_sent_info:
                        # print(directions[self.direction_sent_info])
                        cv2.putText(image, str(directions[self.direction_sent_info]), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                    # 在图像上绘制手部关键点和连线，并显示反馈信息
                    self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)



            # 将图像转换回BGR格式，并显示在窗口中
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imshow("Hand Gesture Recgnition", image)


if __name__ == '__main__':
    hands1=Hands()
    hands1.run_camera()








