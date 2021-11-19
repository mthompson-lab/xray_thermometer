import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler
import matplotlib.pyplot as plt
from itertools import islice
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from numpy.linalg import svd
from numpy.linalg import norm
from sys import argv




class Watcher:
    DIRECTORY_TO_WATCH = argv[1]

    def __init__(self):
        self.observer = Observer()
        self.list_files = []
        print("watching {} and all subfolders for new radial average files in *txt format".format(self.DIRECTORY_TO_WATCH))

    def run(self):
        event_handler = Handler(patterns=["*txt"])
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()      
        plt.ion()  # enter interactive mode
        fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
        fig.suptitle("T-Jump Monitor", fontsize=16)
        plt.draw()  # non-blocking drawing
        plt.pause(.001)  # This line is essential, without it the plot won't be shown

        
        try:
            while True:
                time.sleep(3)
                try:
                    test_one = pd.read_table("t_vals_light.text", header=None)
                    test_two = pd.read_table("t_vals_dark.text", header=None)
                    print("data stream acquired...")
                    if len(test_one) < 500:
                        print("waiting for minimum required data...")
                        break
                    elif len(test_two) < 500:
                        print("waiting for minimum required data...")
                        break
                    else:
                        print("sufficient data acquired...")
                        break

                except:
                    print("waiting for data stream...")
        except:
            print("data acquired - real time monitoring to begin")
                

        try:
            while True:
                time.sleep(5)
                axs[0].cla()
                axs[1].cla()
                t_vals_light = pd.read_table("t_vals_light.text", header=None)
                t_vals_dark = pd.read_table("t_vals_dark.text", header=None)
                axs[0].hist(t_vals_light, bins=50, color='red', label="light", alpha=0.6)
                axs[1].hist(t_vals_light[-500:], bins=10, color='red', label="light - last 500", alpha=0.6)
                axs[0].hist(t_vals_dark, bins=50, color='black', label="dark", alpha=0.6)
                axs[1].hist(t_vals_dark[-500:], bins=10, color='black', label="dark - last 500", alpha=0.6)
                axs[0].legend()
                axs[1].legend()
                axs[0].set_title('Cumulative')
                axs[1].set_title('Last 500 Shots')
                axs[0].set_ylabel("Count")
                plt.tight_layout()
                plt.draw()  # non-blocking drawing
                plt.pause(.001)

        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(PatternMatchingEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            
            def sinc_exp_vec(q_vec_in):
                p1,p2,p3,p4,p5,p6,p7,p8 = [325.08377127,1.80045309,-0.74444932,324.6805628,1.80872365,-0.75487194,2.234949,2.21508248]
                return (p1*np.sinc(p2*q_vec_in+p3)*np.exp(-q_vec_in**p7))-(p4*np.sinc(p5*q_vec_in+p6)*np.exp(-q_vec_in**p8))

            def scale_vector(input_array):
                return np.exp(-input_array)

            print("Received created event - %s." % event.src_path)

            svd_low_q = 1.047
            svd_high_q = 2.649
            scaling_low_q = 2.0
            scaling_high_q = 2.5
            panda_dict = {}
            ordered_keylist = []
            radavg_header_lines = 17
            number_of_radavg_bins = 1189
            image_count = 0
            with open(event.src_path) as f:
                while True:
                    next_n_lines = list(islice(f, number_of_radavg_bins))
                    image_count +=1
                    dataset = pd.DataFrame(list(map(str.split, next_n_lines[radavg_header_lines:-1])), columns = ["q", "I", "sigI"], dtype=float)
                    panda_dict[image_count] = [dataset, "291_x1_r1"] # note that currently the labels are unused...leaving as reference in case it's useful for future applications
                    ordered_keylist.append(image_count)
                    if len(next_n_lines)<10:
                        break

            full_list = []
            lab_list = []

            x = panda_dict[ordered_keylist[0]][0]["q"].values
            refy = scale_vector(x)
            for key in panda_dict:
                y = panda_dict[key][0]["I"].values
                # lab = panda_dict[key][1]
                try:
                    data_mask = np.array(x, dtype=bool)
                    data_mask[x<scaling_low_q]=False
                    data_mask[x>scaling_high_q]=False
                    svd_mask = np.array(x, dtype=bool)
                    svd_mask[x<svd_low_q]=False
                    svd_mask[x>svd_high_q]=False
                    yy = y[data_mask]
                    refyy = refy[data_mask]
                    xx = x[data_mask]
                    q_ref = xx*refyy
                    q_sig = xx*yy
                    top = np.dot(q_sig,q_ref)
                    bottom = np.dot(q_sig,q_sig)
                    scalar = top/bottom
                    temp = y*scalar
                    # temp2 = temp - temp.min()
                    # temp3 = np.divide(temp2,temp2.max())
                    new_x = x[svd_mask]
                    # full_list.append(np.dot(sinc_exp_vec(new_x),temp[svd_mask])/len(new_x))
                    t_val = np.dot(sinc_exp_vec(new_x),temp[svd_mask])/len(new_x)
                    if "light" in event.src_path:
                        with open("t_vals_light.text", "a") as myfile:
                            myfile.write("{}\n".format(t_val))
                    elif "dark" in event.src_path:
                        with open("t_vals_dark.text", "a") as myfile:
                            myfile.write("{}\n".format(t_val))
                    # lab_list.append(lab)
                except:
                    pass

        elif event.event_type == 'modified':
            print("Received modified event - %s." % event.src_path)


if __name__ == '__main__':
    w = Watcher()
    w.run()
