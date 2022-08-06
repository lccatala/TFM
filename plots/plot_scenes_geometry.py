import matplotlib.pyplot as plt

if __name__ == '__main__':
    plt.figure()

    geometry_sizes = [1, 2000, 385079, 262267, 2880000]
    x_values = [x for x in range(len(geometry_sizes))]
    x_labels = ['SingleTriangle', 'VikingRoom', 'BMW', 'CrytekSponza', 'Hairball']
    plt.xticks(x_values, x_labels)
    plt.ylabel('Triangle count')
    plt.bar(x_values, geometry_sizes)
    plt.savefig('scenes-geometry.png')
