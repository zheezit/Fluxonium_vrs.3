import matplotlib.pyplot as plt
import numpy as np
save_plots =False
import string

import matplotlib.transforms as mtransforms

 
# # Creating a series of data of in range of 1-50.
# x = np.linspace(0,10,100)
 
# #Creating a Function.
# def normal_dist(x , mean , sd):
#     prob_density = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
#     return prob_density
 
# hc = 5
# hc1 = 7
# hc2 = 10


# #Calculate mean and Standard deviation.
# mean = np.mean(x)
# sd = np.std(x)
 
# #Apply function to the data.
# pdf = normal_dist(x,mean,sd)
# # print(-pdf[50:100])
 

# # sample data

# x1 = [0,1,2,3,4,5,5.00000001]
# y1 = [0,-1,-2,-3,-4,-5,0]
# x2 = [0, 1, 2, 3, 4, 5, 6, 7]
# y2 = [0,-1,-2,-3,-4,-5,-6,-7]
# labels = ['H_c', 'H_c1', 'H_c2']
# x_ticks = [7,5,10]

# # plotting the graph
# plt.plot(x1, y1, label='Type 1', color='r')

# plt.plot(x2, y2, label='Type 2', color='g')
# plt.plot(x[50:100],-pdf[50:100] , color = 'g')


# # Adding labels and title
# plt.xlabel('External field, H')
# plt.ylabel('Magnetization, M')
# #Plotting the Results



# plt.title('Magnetization vs Critical field')
# plt.legend()

# plt.xticks(x_ticks, labels)
# plt.yticks([])




# # adding vertical lines at critical fields
# plt.axhline(0, color='black', linestyle='-')
# plt.axvline(x=hc, color='r', linestyle='--')
# plt.axvline(x=hc1, color='g', linestyle='--')
# plt.axvline(x=hc2, color='g', linestyle='--')

# # # displaying the graph
# # plt.show()


# # Some example data to display



nrow = 2; ncol = 2;
fig, axs = plt.subplots(nrows=nrow, ncols=nrow, figsize=(8,8))
# axs = np.array(axs)
# axs = axs.flat
# print(axs)

# for n, (key, ax) in enumerate(axs):
#     ax.text(-0.1, 1.1, string.ascii_uppercase[n], transform=ax.transAxes, 
#             size=20, weight='bold')

for label, ax in axs.items():
    trans = mtransforms.ScaledTranslation(10/72, -5/72, fig.dpi_scale_trans)
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans,
            fontsize='medium', verticalalignment='top', fontfamily='serif',
            bbox=dict(facecolor='0.7', edgecolor='none', pad=3.0))

if save_plots:
    fig.savefig('C:images\critical field2.png', bbox_inches = "tight" ,dpi=300)
fig.tight_layout()
plt.show()

