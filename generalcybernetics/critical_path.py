from generalcybernetics.basis import Element, System


def test():

    a1 = Element(payload=2)
    b1 = Element(payload=1)
    c1 = Element(payload=2)

    a2 = Element(payload=2)
    b2 = Element(payload=5)

    a3 = Element(payload=1)

    a1.connect_lr(a2)
    b1.connect_lr(b2)
    c1.connect_lr(b2)

    a2.connect_lr(a3)
    b2.connect_lr(a3)

    inits = [a1, b1, c1]
    priorities = calculate_critical_path(inits)
    for x in priorities:
        print(x)


def calculate_critical_path(inits):
    paths = []
    for x in inits:
        path_sum = 0
        path = []
        while True:
            path_sum += x.payload
            path.append(id(x))
            if len(x.out_connections) == 1:
                x = x.out_connections[0]
            elif len(x.out_connections) > 1:
                # I would have to split the path.
                # needs a different approach.
                raise NotImplementedError
            else:
                break

        paths.append((path, path_sum))
    paths.sort(key=lambda x: x[1])
    return paths


if __name__ == "__main__":
    test()
