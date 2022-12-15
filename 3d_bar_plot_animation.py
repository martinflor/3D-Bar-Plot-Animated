# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 14:45:46 2022

@author: Florian Martin

"""


import imageio.v2 as imageio
from PIL import Image
import PIL.ImageDraw as ImageDraw 
import os
import matplotlib 
from mpl_toolkits import mplot3d
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
from matplotlib.animation import FuncAnimation

class Animation:
    
    def __init__(self):
        
        self.bar_idx = 0
        
    def bar3D(self, xsize, ysize, dz):
        
        xpos, ypos = np.mgrid[0:xsize, 0:ysize]
        xpos, ypos = xpos.ravel(), ypos.ravel()
        zpos = np.zeros(xsize*ysize)
        
        dx, dy = np.ones((xsize,ysize))*0.5, np.ones((ysize,xsize))*0.5
        
        matplotlib.rc('xtick', labelsize=35) 
        matplotlib.rc('ytick', labelsize=35) 
        fig = plt.figure(figsize=(50,50))
        ax = fig.add_subplot(projection='3d')
        cmap = cm.get_cmap('jet')
        max_height = np.max(dz)
        min_height = np.min(dz)
        rgba = [cmap((k-min_height)/max_height) for k in dz.ravel()]
        ax.bar3d(xpos, ypos, zpos, 0.5, 0.5, dz.ravel(), color=rgba)
        
        
        ax.set_zticks(np.arange(50))
        ax.zaxis.set_major_locator(MaxNLocator(integer=True))
    
        ax.set_title(f"\n Instant t = {self.bar_idx}", fontsize=50)
        
        plt.savefig(f"animate/distribution/{self.bar_idx}.jpg")
        self.bar_idx += 1 
        plt.show()

        
    def smooth_bar3D(self, counts, counts_old, number, list_dz, xsize, ysize):
        """
        counts     : the current occurence
        counts_old : the old occurence
        number     : number of frame to smooth the transition between counts_old and counts
        all_dz     : list of dz used in 3dBarPlot of matplotlib
        """
        
        counts_itr = np.copy(counts_old)
        add_count = (counts-counts_old)/number
        for i in range(0, number):
            counts_itr += add_count
            list_dz.append(counts_itr)
            self.bar3D(xsize, ysize, list_dz[-1])
            
    def animate_3dBarPlot(self, nb, fps=60):
        # nb is the number of image saved in the directory "animate/distribution"
        # To save the image use the function bar3D in a loop
        # .jpg to save memory 
        
        frame = []
        for index in range(nb):
            img = imageio.imread(f"animate/distribution/{index}.jpg")
            frame.append(Image.fromarray(img))
    
        imageio.mimwrite(os.path.join('./animate/', f'example_{fps}fps.gif'), frame, fps=60)

    def animate_3dBarPlot2(self, xsize, ysize, all_dz):
        """
        xsize  : size of the grid for the x-axis
        ysize  : size of the grid for the y-axis
        all_dz : list of dz used in 3dBarPlot of matplotlib
        """
        
        xpos, ypos = np.mgrid[0:xsize, 0:ysize]
        xpos, ypos = xpos.ravel(), ypos.ravel()
        zpos = np.zeros(xsize*ysize)
        
        dx, dy = np.ones((xsize,ysize))*0.5, np.ones((ysize,xsize))*0.5
        
        matplotlib.rc('xtick', labelsize=35) 
        matplotlib.rc('ytick', labelsize=35) 
        fig = plt.figure(figsize=(50,50))
        ax = fig.add_subplot(projection='3d')
        ax.zaxis.set_major_locator(MaxNLocator(integer=True))
        
        def update(frame):
            
            dz = all_dz[frame]
        
            ax.set_title(f"\n Instant t = {self.bar_idx}", fontsize=50)
            cmap = cm.get_cmap('jet')
            max_height = np.max(dz)
            min_height = np.min(dz)
            rgba = [cmap((k-min_height)/max_height) for k in dz.ravel()]
            ax.bar3d(xpos, ypos, zpos, 0.5, 0.5, dz.ravel(), color=rgba)
            
            return ax


        anim = FuncAnimation(fig, update, frames=len(all_dz), interval=10)
        anim.save('animate/3dbarPlot.gif')


"""
xsize = 5
ysize = 5 


anim = Animation()
all_dz = []

counts_old = np.random.rand(xsize, ysize)*25 # Number of occurences on the grid for each coordinates
for i in range(5):
    print(i)
    counts = counts_old*2
    anim.smooth_bar3D(counts=counts, 
                      counts_old=counts_old, 
                      number=10, 
                      list_dz=all_dz,
                      xsize=xsize,
                      ysize=ysize)
    
    counts_old = np.random.rand(xsize, ysize)*25
"""  
anim.animate_3dBarPlot(nb=5*10, fps=30) # iteration * number