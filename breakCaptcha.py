import numpy as np
import cv2
from PIL import Image
import zAI
from zAI import zImage

# 이미지 로드
img = cv2.imread('captcha1.png', 0)
#img = cv2.imread('captcha2.png', 0)

# 이미지 대비를 향상
image_enhanced = cv2.equalizeHist(img)

# Adaptive Thresholding 적용
max_output_value = 255   # 출력 픽셀 강도의 최대값
neighborhood_size = 99
subtract_from_mean = 10
image_binarized = cv2.adaptiveThreshold(image_enhanced,
                                       max_output_value,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY,
                                       neighborhood_size,
                                       subtract_from_mean)

# 이미지 not 연산 (흑백 반전)
#horizontal_inv = cv2.bitwise_not(image_binarized)


# and 연산을 수행하여 제공된 마스크로 선을 마스크
masked_img = cv2.bitwise_and(img, img, mask=image_binarized)

# 픽셀 강도의 중간값을 계산
median = np.median(masked_img)

# 중간 픽셀 강도에서 위아래 1 표준편차 떨어진 값을 임곗값으로 지정
lower_threshold = int(max(0, (1.0 - 0.33) * median))
upper_threshold = int(min(255, (1.0 + 0.33) * median))

# Canny edge detection 적용
image_canny = cv2.Canny(masked_img, lower_threshold, upper_threshold)


kernel = np.ones((2,2),np.uint8)
for i in range(1,8):
    dilation = cv2.dilate(image_canny,kernel,iterations = i) # 노이즈 작업 제거 핵심
    cv2.imwrite("img" + str(i) + ".jpg", dilation)


url = "http://" + "capstone4241.cognitiveservices.azure.com/"
# zAI.utils.set_backend_key(key_name='GOOGLE_CLOUD_API_KEY',key_value='(자신의 API키를 넣는다)',save=True)
zAI.utils.set_backend_key(key_name='MICROSOFT_AZURE_VISION_API_KEY', key_value='d9286364fba94a038d460a93ec6a0939', save=True)
zAI.utils.set_backend_key(key_name='MICROSOFT_AZURE_URL', key_value=url, save=True)


# 이미지 지정
image = zImage('img4.jpg')
image.display()

# 이미지 인식
text = image.ocr(backend='Microsoft')
text.display()

