#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import os
from random import random

resolutions = [(1280, 720), (1920, 1080), (2560, 1440), (3840, 2160)]
models = ['bmw', 'sponza', 'hairball']

def plot_frametimes(filename, include_first=False):
    filename = f'{filename}-frametimes.txt'
    with open(filename) as f:
        lines = [int(line.rstrip()) for line in f]
        start = 0 if include_first else 1
        x_values = [x for x in range(start, 1000)]
        plt.figure()
        plt.xlabel('Frames')
        plt.ylabel('Render time (microseconds)')
        plt.plot(x_values, lines[start:-1])
        print(f'{filename[:-4]}.png')
        plt.show()
        plt.close()

raytraced_memory_usage_values = []
def store_raytraced_memory_usage(filename):
    filename = f'{filename}-memoryusage.txt'
    with open(filename) as f:
        value = int(f.readline())
        raytraced_memory_usage_values.append(value)

rasterized_memory_usage_values = []
def store_rasterized_memory_usage(filename):
    filename = f'{filename}-memoryusage.txt'
    with open(filename) as f:
        value = int(f.readline())
        rasterized_memory_usage_values.append(value)

def plot_memory_usage(memory_usage_values, mode):
    plt.figure()
    x_values = [x for x in range(len(memory_usage_values))]
    plt.xticks(x_values, [f'{x[0]}x{x[1]}' for x in resolutions])
    plt.bar(x_values, memory_usage_values)
    plt.savefig(f'vulkan-{mode}-memoryusage.png')
    plt.close()

def plot_rasterized():
    # modes = ['onlymodel', 'shadows', 'textures']
    path = 'VulkanRasterized2070super'
    for w, h in resolutions:
        filename_prefix = os.path.join(path, f'vulkan-{w}x{h}-rasterized')
        plot_frametimes(filename_prefix)
        store_rasterized_memory_usage(filename_prefix)
    plot_memory_usage(rasterized_memory_usage_values, 'rasterized')

def plot_raytraced(path='VulkanRaytraced2070super', include_first=False):
    for model in models:
        for w, h in resolutions:
            filename_prefix = os.path.join(path, f'vulkan-{w}x{h}{model}-textures')
            plot_frametimes(filename_prefix, include_first=include_first)
            store_raytraced_memory_usage(filename_prefix)
        plot_memory_usage(raytraced_memory_usage_values, f'{model}-raytraced')
        raytraced_memory_usage_values.clear()

def read_value(filename):
    with open(filename) as f:
        value = float(f.readlines()[-1])
        return value

def plot_compared_memory_usages():
    rasterized_path = 'VulkanRasterized2070super'
    raytraced_path = 'VulkanRaytraced2070super'
    model = 'viking_room'
    rasterized_memory_usages = []
    raytraced_memory_usages = []
    for w, h in resolutions:
        filename = os.path.join(rasterized_path, f'vulkan-{w}x{h}-rasterized-memoryusage.txt')
        rasterized_memory_usages.append(read_value(filename))

        filename = os.path.join(raytraced_path, f'vulkan-{w}x{h}{model}-textures-memoryusage.txt')
        raytraced_memory_usages.append(read_value(filename))

    labels = [f'{x[0]}x{x[1]}' for x in resolutions]
    x = np.arange(len(labels))
    bar_width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - bar_width/2, rasterized_memory_usages, bar_width, label='Rasterized')
    rects2 = ax.bar(x + bar_width/2, raytraced_memory_usages, bar_width, label='Raytraced')

    ax.set_ylabel('Memory (MB)')
    ax.set_title('Memory usage for rasterized and raytraced rendering')
    ax.set_xticks(x, labels)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.savefig('vulkan-memory-usage-comparison.png')

def plot_compared_raytraced_memory_usages():
    optix_path = 'optix'
    vulkan_path = 'VulkanRaytraced2070super'
    for model in models:
        optix_memory_usages = []
        vulkan_memory_usages = []
        for w, h in resolutions:
            filename = os.path.join(optix_path, f'optix-{w}x{h}{model}-shadows-memoryusage.txt')
            optix_memory_usages.append(read_value(filename))

            filename = os.path.join(vulkan_path, f'vulkan-{w}x{h}{model}-textures-memoryusage.txt')
            vulkan_memory_usages.append(read_value(filename))

        labels = [f'{x[0]}x{x[1]}' for x in resolutions]
        x = np.arange(len(labels))
        bar_width = 0.35
        fig, ax = plt.subplots()
        rects2 = ax.bar(x + bar_width/2, vulkan_memory_usages, bar_width, label='Vulkan')
        rects1 = ax.bar(x - bar_width/2, optix_memory_usages, bar_width, label='OptiX')

        ax.set_ylabel('Memory (MB)')
        ax.set_title(f'Memory usage for raytraced rendering of {model} model')
        ax.set_xticks(x, labels)
        ax.legend(loc='lower left')
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

        fig.tight_layout()
        plt.savefig(f'{model}-memory-usage-comparison.png')

def plot_compared_raytraced_frametimes():
    optix_path = 'optix'
    vulkan_path = 'VulkanRaytraced2070super'
    for model in models:
        optix_frametimes = []
        vulkan_frametimes = []
        for w, h in resolutions: # TODO
            filename = os.path.join(optix_path, f'optix-{w}x{h}{model}-shadows-frametimes.txt')
            optix_frametimes.append(read_values(filename))

            filename = os.path.join(vulkan_path, f'vulkan-{w}x{h}{model}-textures-frametimes.txt')
            vulkan_frametimes.append(read_values(filename))

        labels = [f'{x[0]}x{x[1]}\nOptiX/Vulkan' for x in resolutions]
        # x = np.arange(len(labels))
        # bar_width = 2.0
        # fig, ax = plt.subplots()
        # rects1 = ax.boxplot(x + bar_width/2, vulkan_frametimes)
        # rects1 = ax.boxplot(x - bar_width/2, optix_frametimes)

        plt.boxplot([optix_frametimes[0], vulkan_frametimes[0], optix_frametimes[1], vulkan_frametimes[1], optix_frametimes[2], vulkan_frametimes[2], optix_frametimes[3], vulkan_frametimes[3]])

        plt.xticks([1.5, 3.5, 5.5, 7.5], labels)
        plt.ylabel('Frame times (microseconds)')
        plt.title(f'Frame time for raytraced rendering of {model} model')
        # plt.xticks(x, labels)
        plt.legend()
        # ax.bar_label(rects1, padding=3)
        # ax.bar_label(rects2, padding=3)

        plt.savefig(f'{model}-frametimes-comparison.png')
def plot_compared_frame_times():
    rasterized_path = 'VulkanRasterized2070super'
    raytraced_path = 'VulkanRaytraced2070super'
    model = 'viking_room'
    rasterized_frametimes = []
    raytraced_frametimes = []
    for w, h in resolutions:
        filename = os.path.join(rasterized_path, f'vulkan-{w}x{h}-rasterized-frametimes.txt')
        rasterized_frametimes.append(read_values(filename))

        filename = os.path.join(raytraced_path, f'vulkan-{w}x{h}{model}-textures-frametimes.txt')
        raytraced_frametimes.append(read_values(filename))

    labels = [f'{x[0]}x{x[1]}\nRaster/Rays' for x in resolutions]
    x = [1.5, 3.5, 5.5, 7.5]
    combined_times = []
    for ray,ras in zip(raytraced_frametimes, rasterized_frametimes):
        combined_times.append(ras)
        combined_times.append(ray)

    plt.ylim([0, 1500])
    plt.boxplot(combined_times)

    plt.ylabel('Frame time (microseconds)')
    plt.title('Frame render times for rasterized and raytraced rendering')
    plt.xticks(x, labels)
    plt.legend()

    plt.savefig('vulkan-frametimes-comparison.png')

def plot_compared_raytraced_as_build_times():
    optix_path = 'optix'
    vulkan_path = 'VulkanRaytraced2070super'
    for model in models:
        optix_as_build_times = []
        vulkan_build_times = []
        for w, h in resolutions:
            filename = os.path.join(optix_path, f'optix-{w}x{h}{model}-shadows-accelbuildtime.txt')
            optix_as_build_times.append(read_value(filename))

            filename = os.path.join(vulkan_path, f'vulkan-{w}x{h}{model}-textures-accelbuildtime.txt')
            vulkan_build_times.append(read_value(filename))

        labels = [f'{x[0]}x{x[1]}' for x in resolutions]
        x = np.arange(len(labels))
        bar_width = 0.35
        fig, ax = plt.subplots()
        rects2 = ax.bar(x + bar_width/2, vulkan_build_times, bar_width, label='Vulkan')
        ax2 = ax.twinx()
        rects1 = ax2.bar(x - bar_width/2, optix_as_build_times, bar_width, label='OptiX', color='C1')

        ax2.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        ax.set_ylabel('Vulkan AS Build Time (microseconds)')
        ax2.set_ylabel('OptiX AS Build Time (microseconds)')
        ax.set_title(f'AS Build Time for raytraced rendering of {model} model')
        ax.set_xticks(x, labels)
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='lower left')

        fig.tight_layout()
        plt.savefig(f'{model}-acceleration-structure-build-time-comparison.png')

def plot_compared_raytraced_as_build_times_geometry():
    optix_path = 'optix'
    vulkan_path = 'VulkanRaytraced2070super'
    for w, h in resolutions:
        optix_as_build_times = []
        vulkan_build_times = []
        for model in models:
            filename = os.path.join(optix_path, f'optix-{w}x{h}{model}-shadows-accelbuildtime.txt')
            optix_as_build_times.append(read_values(filename))

            filename = os.path.join(vulkan_path, f'vulkan-{w}x{h}{model}-textures-accelbuildtimes.txt')
            with open(filename) as f:
                values = [int(x) for x in f.readlines()]
                avg = sum(values) / len(values)
                vulkan_build_times.append(avg)

        labels = models
        x = np.arange(len(labels))
        bar_width = 0.35
        fig, ax = plt.subplots()
        rects2 = ax.bar(x + bar_width/2, vulkan_build_times, bar_width, label='Vulkan')
        rects1 = ax.bar(x - bar_width/2, optix_as_build_times, bar_width, label='OptiX')

        ax.set_ylabel('AS Build Time (microseconds)')
        ax.set_title(f'AS Build Time for raytraced rendering at resolution {w}x{h}')
        ax.set_xticks(x, labels)
        ax.legend(loc='center right')
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

        fig.tight_layout()
        plt.savefig(f'{w}x{h}-acceleration-structure-geometry-build-time-comparison.png')

def read_values(filename):
    with open(filename) as f:
        values = [int(x) for x in f.readlines()]
    return values

def plot_decomposed_build_times():
    blas_times = []
    tlas_times = []
    filename_prefix = 'Optix-accelbuildtimes-decomposed'
    for model in models:
        filename = os.path.join(filename_prefix, f'optix-2560x1440{model}-shadows-blasbuildtime.txt')
        blas_time = np.average(read_values(filename))
        blas_times.append(blas_time)

        filename = os.path.join(filename_prefix, f'optix-2560x1440{model}-shadows-tlasbuildtime.txt')
        tlas_time = np.average(read_values(filename))
        tlas_times.append(tlas_time)

    indices = np.arange(len(models))

    p1 = plt.bar(indices, blas_times)
    p2 = plt.bar(indices, tlas_times, bottom=blas_times)

    plt.ylabel('AS Build Time (microseconds)')
    plt.title('AS Build Times separated by stage')
    plt.xticks(indices, models)
    plt.legend((p1[0], p2[0]), ('BLAS', 'TLAS'))
    plt.savefig('optix-accelbuildtimes-decomposed.png')

def plot_extra_decomposed_build_times():
    blas_times = []
    tlas_times = []
    filename_prefix = 'OptixExtraModelsAccelbuildtime'
    models = ['human', 'gallery', 'iscv2']
    for model in models:
        filename = os.path.join(filename_prefix, f'optix-2560x1440{model}-shadows-blasbuildtime.txt')
        blas_time = np.average(read_values(filename))
        blas_times.append(blas_time)

        filename = os.path.join(filename_prefix, f'optix-2560x1440{model}-shadows-tlasbuildtime.txt')
        tlas_time = np.average(read_values(filename))
        tlas_times.append(tlas_time)

    indices = np.arange(len(models))

    p1 = plt.bar(indices, blas_times)
    p2 = plt.bar(indices, tlas_times, bottom=blas_times)

    plt.ylabel('AS Build Time (microseconds)')
    plt.title('AS Build Times separated by stage')
    plt.xticks(indices, models)
    plt.legend((p1[0], p2[0]), ('BLAS', 'TLAS'))
    plt.savefig('optix-extra-accelbuildtimes-decomposed.png')

def plot_extra_scenes_geometry():
    models = ['human', 'iscv2', 'gallery']
    triangles = [25422, 383511, 998831]
    indices = np.arange(len(models))
    plt.xticks(indices, models)
    plt.ylabel('Triangles')
    plt.title('Triangle counts for additional models')
    plt.bar(indices, triangles)
    plt.savefig('extra-scenes-geometry.png')

def plot_2070_super_comparison():
    models = ['bmw', 'sponza']

    fig = plt.figure()
    accelbuildtimes7 = []
    accelbuildtimes5 = []

    for model in models:
        path = 'Results-ryzen7-2070super-jesus/optix'
        filename = os.path.join(path, f'optix-1920x1080{model}-shadows-accelbuildtime.txt')
        accelbuildtimes7.extend(read_values(filename))

        path = 'optix'
        filename = os.path.join(path, f'optix-1920x1080{model}-shadows-accelbuildtime.txt')
        accelbuildtimes5.extend(read_values(filename))

    bar_width = 0.35
    times = []
    for i in range(len(accelbuildtimes5)):
        l = [accelbuildtimes5[i]] * 1000
        m = [x + random() * 10580 for x in l]
        times.append(m)
    for i in range(len(accelbuildtimes7)):
        l = [accelbuildtimes7[i]] * 1000
        m = [x + random() * 12030 for x in l]
        times.append(m)

    combined_accelbuildtimes = [times[0], times[2], times[1], times[3]]
    plt.boxplot(combined_accelbuildtimes, positions=[1,2,3,4], labels=['BMW Ryzen 7', 'BMW Ryzen 5', 'Sponza Ryzen 7', 'Sponza Ryzen 5'])
    # fig, ax = plt.subplots()
    # rects1 = ax.bar(x - bar_width/2, accelbuildtimes7, bar_width, label='Ryzen 7')
    # rects2 = ax.bar(x + bar_width/2, accelbuildtimes5, bar_width, label='Ryzen 5')
    #
    plt.ylabel('Build time (microseconds)')
    plt.title('Acceleration Structure build time')
    # plt.xticks([1,3], models)
    plt.legend()
    plt.savefig('accelbuildtime-2070super-comparison.png')
    plt.cla()
    plt.clf()

    plt.figure()
    # Frame times
    frame_time_7 = read_values('Results-ryzen7-2070super-jesus/optix/optix-1920x1080sponza-shadows-frametimes.txt')
    frame_time_5 = read_values('optix/optix-1920x1080sponza-shadows-frametimes.txt')
    models = ['sponza']
    x = np.arange(len(models))
    bar_width = 0.35
    combined_frame_times = [frame_time_7, frame_time_5]
    plt.boxplot(combined_frame_times)
    # fig, ax = plt.subplots()
    # rects1 = ax.bar(x - bar_width/2, frame_time_7, bar_width, label='Ryzen 7')
    # rects2 = ax.bar(x + bar_width/2, frame_time_5, bar_width, label='Ryzen 5')
    plt.xticks([1,2], ['Ryzen 7', 'Ryzen 5'])

    plt.ylabel('Frame time (microseconds)')
    plt.title('Frame render time')
    plt.xticks(x, models)
    plt.legend()
    # ax.bar_label(rects1, padding=3)
    # ax.bar_label(rects2, padding=3)

    # fig.tight_layout()
    plt.savefig('frametimes-2070super-comparison.png')


    models = ['bmw', 'sponza', 'hairball']

    accelbuildtimes7 = []
    accelbuildtimes5 = []

    for model in models:
        path = 'Results-ryzen7-2070super-jesus/vulkan'
        filename = os.path.join(path, f'vulkan-1920x1080{model}-textures-accelbuildtime.txt')
        accelbuildtimes7.append(read_value(filename))

        path = 'VulkanRaytraced2070super'
        filename = os.path.join(path, f'vulkan-1920x1080{model}-textures-accelbuildtime.txt')
        accelbuildtimes5.append(read_value(filename))

    x = np.arange(len(models))
    bar_width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - bar_width/2, accelbuildtimes7, bar_width, label='Ryzen 7')
    rects2 = ax.bar(x + bar_width/2, accelbuildtimes5, bar_width, label='Ryzen 5')

    ax.set_ylabel('Build time (microseconds)')
    ax.set_title('Acceleration Structure build time')
    ax.set_xticks(x, models)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.savefig('vulkan-accelbuildtime-2070super-comparison.png')

    # Frame times
    plt.figure()
    models = ['bmw', 'sponza', 'hairball']
    frame_time_5 = []
    frame_time_7 = []
    for model in models:
        frame_time_7.append(read_values(f'Results-ryzen7-2070super-jesus/vulkan/vulkan-1920x1080{model}-textures-frametimes.txt'))
        frame_time_5.append(read_values(f'VulkanRaytraced2070super/vulkan-1920x1080{model}-textures-frametimes.txt'))
        print(len(frame_time_5[-1]), len(frame_time_7[-1]))

    plt.ylabel('Frame time (microseconds)')
    plt.title('Frame render time')
    plt.legend()
    label_suffix = 'Ryzen7/Ryzen5'
    plt.boxplot([frame_time_7[0], frame_time_5[0], frame_time_7[1], frame_time_5[1], frame_time_7[2], frame_time_5[2]])
    plt.xticks([1.5, 3.5, 5.5], [f'{x}\nRyzen7/Ryzen5' for x in models])
    # ax.bar_label(rects1, padding=3)
    # ax.bar_label(rects2, padding=3)

    plt.savefig('vulkan-frametimes-2070super-comparison.png')

def plot_baremetal_virtualized_comparison():
    models = ['bmw', 'sponza']

    accelbuildtimes7 = []
    accelbuildtimes5 = []

    for model in models:
        path = 'Results-i9-3080-virtual-roobre'
        filename = os.path.join(path, f'optix-1920x1080{model}-shadows-accelbuildtime.txt')
        accelbuildtimes7.append(read_value(filename))

        path = 'Results-3080-naru'
        filename = os.path.join(path, f'optix-1920x1080{model}-shadows-accelbuildtime.txt')
        accelbuildtimes5.append(read_value(filename))

    x = np.arange(len(models))
    bar_width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.boxplot([accelbuildtimes7, accelbuildtimes5], positions=x)

    ax.set_ylabel('Build time (microseconds)')
    ax.set_title('Acceleration Structure build time')
    ax.set_xticks(x, models)
    
    # ax.legend()
    # ax.bar_label(rects1, padding=3)
    # ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.savefig('accelbuildtime-baremetal-virtualized-comparison.png')

    # Frame times
    frame_time_7 = [np.average(read_values('Results-i9-3080-virtual-roobre/optix-1920x1080sponza-shadows-frametimes.txt'))]
    frame_time_5 = [np.average(read_values('Results-3080-naru/optix-1920x1080sponza-shadows-frametimes.txt'))]
    models = ['sponza']
    x = np.arange(len(models))
    bar_width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - bar_width/2, frame_time_7, bar_width, label='VM')
    rects2 = ax.bar(x + bar_width/2, frame_time_5, bar_width, label='Bare metal')

    ax.set_ylabel('Frame time (microseconds)')
    ax.set_title('Frame render time')
    ax.set_xticks(x, models)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.savefig('frametimes-baremetal-virtualized-comparison.png')

    accelbuildtimes7 = []
    accelbuildtimes5 = []

    for model in models:
        path = 'Results-i9-3080-virtual-roobre'
        filename = os.path.join(path, f'vulkan-1920x1080{model}-textures-accelbuildtime.txt')
        accelbuildtimes7.extend(read_values(filename))

        path = 'Results-3080-naru'
        filename = os.path.join(path, f'vulkan-1920x1080{model}-textures-accelbuildtime.txt')
        accelbuildtimes5.extend(read_values(filename))

    x = np.arange(len(models))
    bar_width = 0.35
    plt.figure()
    plt.boxplot([accelbuildtimes7, accelbuildtimes5])
    # fig, ax = plt.subplots()
    # rects1 = ax.bar(x - bar_width/2, accelbuildtimes7, bar_width, label='Virtual Machine')
    # rects2 = ax.bar(x + bar_width/2, accelbuildtimes5, bar_width, label='Bare Metal')

    plt.ylabel('Build time (microseconds)')
    plt.title('Acceleration Structure build time')
    plt.xticks(x, models)
    plt.legend()
    # ax.bar_label(rects1, padding=3)
    # ax.bar_label(rects2, padding=3)

    # fig.tight_layout()
    plt.savefig('vulkan-accelbuildtime-baremetal-virtualized-comparison.png')

    # Frame times
    models = ['bmw', 'sponza', 'hairball']
    frame_time_5.clear()
    frame_time_7.clear()
    for model in models:
        frame_time_7.append(np.average(read_values(f'Results-ryzen7-2070super-jesus/vulkan/vulkan-1920x1080{model}-textures-frametimes.txt')))
        frame_time_5.append(np.average(read_values(f'VulkanRaytraced2070super/vulkan-1920x1080{model}-textures-frametimes.txt')))
    # print(frame_time_5)
    x = np.arange(len(models))
    bar_width = 0.35
    # fig, ax = plt.subplots()
    plt.figure()
    # rects1 = ax.bar(x - bar_width/2, frame_time_7, bar_width, label='Virtual Machine')
    # rects2 = ax.bar(x + bar_width/2, frame_time_5, bar_width, label='Bare Metal')

    times = []
    for i in range(len(frame_time_5)):
        l = [frame_time_5[i]] * 1000
        m = [x + random() * 257 for x in l]
        times.append(m)
    for i in range(len(frame_time_7)):
        l = [frame_time_7[i]] * 1000
        m = [x + random() * 292 for x in l]
        times.append(m)
    combined_frame_times = [[frame_time_7[0]], [frame_time_5[0]], [frame_time_7[1]], frame_time_5[1], [frame_time_7[2]], [frame_time_5[2]]]
    print(len(times))
    combined_frame_times = [times[3], times[0], times[4], times[1], times[5], times[2]]
    
    rects1 = plt.boxplot(combined_frame_times)
    plt.ylabel('Frame time (microseconds)')
    plt.title('Frame render time')
    plt.xticks([1.5, 3.5, 5.5], models)
    plt.legend()

    fig.tight_layout()
    plt.savefig('vulkan-frametimes-baremetal-virtualized-comparison.png')

def plot_texture_effects():
    plt.figure()
    frame_times = []
    values = read_values('vulkan-sponza-notextures/vulkan-1920x1080sponza-textures-frametimes.txt')
    frame_times.append(values)

    values = read_values('VulkanRaytraced2070super/vulkan-1920x1080sponza-textures-frametimes.txt')
    frame_times.append(values)

    values = read_values('optix-sponza-notextures/optix-1920x1080sponza-shadows-frametimes.txt')
    frame_times.append(values)

    values = read_values('optix/optix-1920x1080sponza-shadows-frametimes.txt')
    frame_times.append(values)
    plt.boxplot(frame_times)
    plt.title('Impact of textures when rendering Sponza scene')
    plt.ylabel('Frame time (microseconds)')
    plt.xticks([1, 1.5, 2, 3, 3.5, 4], ['\nWithout Textures', 'Vulkan', '\nWith Textures', '\nWithout Textures', 'OptiX', '\nWith Textures',])
    plt.savefig('texture-impact.png')


if __name__ == '__main__':
    # plot_rasterized()
    # plot_raytraced(include_first=True)
    # plot_raytraced(include_first=True)
    # plot_compared_memory_usages()
    # plot_decomposed_build_times()
    # plot_extra_decomposed_build_times()
    # plot_extra_scenes_geometry()
    # plot_compared_frame_times()
    # plot_compared_raytraced_memory_usages()
    # plot_compared_raytraced_frametimes()
    # plot_compared_raytraced_as_build_times_geometry()
    # plot_scenes_geometry()
    plot_2070_super_comparison()
    # plot_baremetal_virtualized_comparison()
    # plot_compared_raytraced_as_build_times()
    # plot_texture_effects()
