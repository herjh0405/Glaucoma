def rgb(minimum, maximum, value):
        minimum, maximum = float(minimum), float(maximum)

        if value == 0.1 :
            r = 255
            g = 255
            b = 255
        else :
            ratio = 2 * (value-minimum) / (maximum - minimum)
            b = int(max(0, 255*(1 - ratio)))
            r = int(max(0, 255*(ratio - 1)))
            g = 255 - b - r
        return r, g, b
    
def filter_person(pid, eye, value):
    pid_person = df_4[(df_4['PID']==pid) & (df_4['Eye']==eye)]
    part_list = list(filter(lambda x : value in x, pid_person.columns))
    
    global filter_data
    filter_data = pid_person[['PID','AGE','Eye','Exam Date']+part_list]
    
def show_eye(pid, eye, value):
    filter_person(pid, eye, value)
    print(list(filter_data['Exam Date']))

    input_date = input()
    vis_data = filter_data[filter_data['Exam Date']==int(input_date)]
    
    if vis_data['Eye'].iloc[0] == 'OS' : 
        visual_value = pd.DataFrame({input_date : [0.1]*72})
        ind_val = 0
        for i in range(72):
            if (i<2) or (6<=i<10) or (16<=i<18) or (i==26) or (53<=i<55) or (61<=i<65) or (69<=i):
                visual_value[input_date][i] = 0.1
            else :
                visual_value[input_date][i] = vis_data.iloc[:,-54:].values[0][ind_val]
                ind_val += 1
                
    elif vis_data['Eye'].iloc[0] == 'OD': 
        visual_value = pd.DataFrame({input_date : [0.1]*72})
        ind_val = 0
        for i in range(72):
            if (i<3) or (7<=i<11) or (17<=i<19) or (i==45) or (54<=i<56) or (62<=i<66) or (70<=i):
                visual_value[input_date][i] = 0.1
            else :
                visual_value[input_date][i] = vis_data.iloc[:,-54:].values[0][ind_val]
                ind_val += 1

    use_val = visual_value.values
    img = np.zeros((400, 450, 3), np.uint8)

    ext_ind = 0
    for i in range(72):
        if ext_ind == 0 :
            point1 = 50*i, 0
        else : point1 = 50*(i-9*ext_ind), 0+50*ext_ind
        point2 = point1[0]+50, point1[1]+50
        point3 = point1[0]+7, point1[1]+25
        img = cv2.rectangle(img, point1, point2, rgb(min(use_val), max(use_val), use_val[i]), -1)
        img = cv2.putText(img, str(use_val[i][0]), point3, 16, 0.4, (255, 255, 255), thickness =2)

        if (i%9==8):
            ext_ind += 1

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # cv2.imshow(input_date, imgRGB)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    plt.imshow(imgRGB)
    plt.show()