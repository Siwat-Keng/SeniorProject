def createDummy(x, n):
    for i in range(n):
        for j in range(n):
            if i > 0 and j > 0 and i < n-1 and j < n-1:
                x.add_path((i, j), (i-1, j))
                x.add_path((i, j), (i+1, j))
                x.add_path((i, j), (i, j-1))
                x.add_path((i, j), (i, j+1))
            elif i == 0 and j == 0 and n > 1:
                x.add_path((0, 0), (0, 1))
                x.add_path((0, 0), (1, 0))
            elif i == 0 and j == n-1 and n > 1:
                x.add_path((i, j), (i+1, j))
                x.add_path((i, j), (i, j-1))
            elif i == n-1 and j == 0 and n > 1:
                x.add_path((i, j), (i-1, j))
                x.add_path((i, j), (i, j+1))
            elif i == n-1 and j == n-1 and n > 1:
                x.add_path((i, j), (i-1, j))
                x.add_path((i, j), (i, j-1))
            elif i == 0 and j != n-1 and j != 0 and n > 1:
                x.add_path((i, j), (i+1, j))
                x.add_path((i, j), (i, j-1))
                x.add_path((i, j), (i, j+1))
            elif j == 0 and i != n-1 and i != 0 and n > 1:
                x.add_path((i, j), (i-1, j))
                x.add_path((i, j), (i+1, j))
                x.add_path((i, j), (i, j+1))
            elif i == n-1 and j != n-1 and j != 0 and n > 1:
                x.add_path((i, j), (i-1, j))
                x.add_path((i, j), (i, j-1))
                x.add_path((i, j), (i, j+1))
            elif j == n-1 and i != n-1 and i != 0 and n > 1:
                x.add_path((i, j), (i-1, j))
                x.add_path((i, j), (i+1, j))
                x.add_path((i, j), (i, j-1))


if __name__ == '__main__':
    import time
    from Navigation import Navigation
    navigation = Navigation()
    t = time.time()
    n = int(input('Enter map size: '))
    createDummy(navigation, n)
    print('Created Map in {}s'.format(time.time()-t))
    navigation.set_position(0, 0)
    navigation.set_goal(n-1, n-1)
    t = time.time()
    navigation.del_node((n//4, n//4))
    navigation.del_node((n*3//4, n//4))
    navigation.del_node((n//4, n*3//4))
    navigation.del_node((n*3//4, n*3//4))
    navigation.remove_all_path((n//2, n//2))
    print('Modified Map in {}s'.format(time.time()-t))
    t = time.time()
    navigation.calculate_shortest_path()
    print('Calculated path in {}s'.format(time.time()-t))
    while not navigation.at_destination():
        input()
        print(navigation.navigate())
    print('Done')
    # t = time.time()
    # navigation.calculate_all_path()
    # print('Calculated path in {}s'.format(time.time()-t))
