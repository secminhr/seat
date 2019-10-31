class Method:
    def move_left(self, index, arr, num):
        raise NotImplementedError('This method cannot be called on Method class itself')

    def move_right(self, index, arr, num):
        raise NotImplementedError('This method cannot be called on Method class itself')

class inst(Method):
    def move_left(self, index, arr, num):
        arr.insert(index-num,arr.pop(index))
        return arr
    
    def move_right(self, index, arr, num):
        arr.insert(index+num, arr.pop(index))
        return arr

class swap(Method):
    def move_left(self, index, arr, num):
        arr[index], arr[index-num]=arr[index-num], arr[index]
        return arr

    def move_right(self, index, arr, num):
        arr[index], arr[index+num]=arr[index+num], arr[index]
        return arr

class push(Method):
    def move_left(self, index, arr, num):
        return arr[num:]+arr[:num]

    def move_right(self, index, arr, num):
        return arr[-num:]+arr[:-num]