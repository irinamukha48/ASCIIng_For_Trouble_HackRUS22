import cv2
import numpy as np
import tkinter
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from tkinter import filedialog


if __name__ == '__main__':
    successfullyOpen = False
    ascii_color = (255, 255, 255)
    bg_color = (0, 0, 0)

    for index in range(-1, 10):
        vid = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if vid.isOpened():
            successfullyOpen = True
            break

    if successfullyOpen:
        shades = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
        shades_list = shades.split()

        root = tkinter.Tk()
        messagebox.showinfo("Camera found!", "Welcome to...!\n- To quit the program, hold 'q'\n- To change the color "+
                                             "of the ASCII, hold 'a'\n- To change the color of the square, hold 'b'\n"+
                            "- To save the image to your computer, hold 's'")
        root.destroy()

        while True:
            ret, frame = vid.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            haar_face_cascade = cv2.CascadeClassifier('venv/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml')
            faces = haar_face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), bg_color, -1)
                scaled_gray = cv2.resize(gray, (int(w/4), int(h/4)), 0, 0)
                im = np.array(scaled_gray)

                # scale to scaled image
                scaled_left = int(x * int(w/4)/640)
                scaled_top = int(y * int(h/4)/480)
                scaled_width = int(w * int(w/4)/640)
                scaled_height = int(h * int(h/4)/480)

                for row in range(scaled_top, scaled_top+scaled_height):
                    for pixel in range(scaled_left, scaled_left+scaled_width):
                        string_show = str(shades[int((255-im[row][pixel]-1)/3.64)])
                        cv2.putText(frame, string_show, (x + int(640/int(w/4)) * (pixel - scaled_left), y +
                                                         int(480/int(h/4)) * (row - scaled_top) + 15),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.35,
                                    ascii_color, 1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(1) & 0xFF == ord('a'):
                root = tkinter.Tk()
                rgb_color = askcolor()[0]
                ascii_color = (rgb_color[2], rgb_color[1], rgb_color[0])
                root.destroy()
            elif cv2.waitKey(1) & 0xFF == ord('b'):
                root = tkinter.Tk()
                rgb_color = askcolor()[0]
                bg_color = (rgb_color[2], rgb_color[1], rgb_color[0])
                root.destroy()
            elif cv2.waitKey(1) & 0xFF == ord('s'):
                root = tkinter.Tk()
                filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG image", "*.png"),
                                                                                            ("JPEG image", "*.jpeg")])
                try:
                    cv2.imwrite(filename, frame)
                except:
                    messagebox.showerror("Error", "No filename selected - saving failed")
                root.destroy()
            cv2.putText(frame, "'q' - quit", (10, int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))-80), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)
            cv2.putText(frame, "'a' - ASCII color", (10, int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)) - 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)
            cv2.putText(frame, "'b' - square color", (10, int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)) - 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)
            cv2.putText(frame, "'s' - save frame", (10, int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)) - 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)
            cv2.imshow('Frame', frame)

        # After the loop release the cap object
        vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
    else:
        messagebox.showerror("Error", "No available camera")
