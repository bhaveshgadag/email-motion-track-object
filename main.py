import cv2
from send_email import send_email
from glob import glob

camera = cv2.VideoCapture(0)

first_frame = None
status_list = []
count = 1

while True:
    check, frame = camera.read()
    status = 0

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/image_{count}.png", frame)
            count = count + 1
            all_images = glob("images/*.png")
            index = int(len(all_images) / 2)
            object_image = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email(object_image)
    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

camera.release()
