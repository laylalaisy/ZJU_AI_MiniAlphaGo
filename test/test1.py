import pickle


class A:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def f(self):
        print(self.name, self.age)


def read():
    with open('abc.pkl', 'rb') as f:
        aa = pickle.load(f)
        # aa.f()
        print(aa)
        print(type(aa))
        return aa


def write():
    with open('abc.pkl', 'wb') as f:
        a_person = A('abc', 22)
        pickle.dump(a_person, f)


def f(pre_move):
    if pre_move is None:
        print('none')
    else:
        print('not none')


if __name__ == '__main__':
    f((None, None))
