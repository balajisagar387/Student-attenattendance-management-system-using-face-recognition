"""img_id=100
             id = self.var_id.get()
             
             
             file_name = r"data\user."+str(id)+"."+str(img_id)+".jpg"
             
             target="data"
             for file in os.listdir(target) :
                     if img_id<=100:
                         img_id=+1
                         if file.startswith("user."+str(id)+"."+str(img_id)):
                             os.remove(file) """
