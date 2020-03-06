import random
import time

# A survey of sorting algorithms
# written as a review of coding concepts

def is_in_order(lst,lo,hi,comp):
    for ind in range(lo,hi-1):
        if comp(lst[ind],lst[ind+1])>0: return False
    return True

def swap(lst,a,b):
    """Swap elements lst[a] and lst[b]"""
    temp = lst[a]
    lst[a] = lst[b]
    lst[b] = temp
    del temp

def mk_lsts(size,n):
    """List of integer lists of specified size. Of those n lists,
       one is in ascending order, and another is in descending order."""
    lsts = []
    lst_one = []
    for i in range(size):
        lst_one.append(i)
    lsts.append(lst_one)
    for _ in range(n-2):
        lsts.append(random.sample(lsts[0],size))
    lsts.append(lsts[0][::-1])
    return lsts

def cmp(x,y):
    return x-y

size = 2000
trials = 20

class TimeoutException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class Sorter(object):
    def __init__(self, comp):
        # comp is the function of type (a,a)->{-1,0,1}
        self.comp = comp
        self.name = 'Default sort'

    def __str__(self):
        """ Test the given sort and print the results of it """
        lsts = mk_lsts(size,trials)
        t_sum = 0
        error = 0
        for lst in lsts:
            sort_time = self.time_sort(lst)
            assert is_in_order(lst,0,size,self.comp)
            if type(sort_time) == float:
                t_sum+=sort_time
            else: error+=1
        avg = t_sum/(trials-error)
        return self.name + ' sorting took ' + str(avg) + \
                 ' seconds to execute!\n' + '  There were ' + \
                 str(error) + '/20 timeouts.'
    
    def sort(self, lst):
        """ Default sort """
        lst.sort()
    
    def time_sort(self, lst):
        # try:
        start = time.time()
        self.sort(lst)
        return time.time() - start
        # except TimeoutException:
        #     return 'too many'

class QuickSorter(Sorter):
    def __init__(self, comp):
        Sorter.__init__(self,comp)
        self.name = 'QuickSort'

    def partition(self,lst,lo,hi,comp):
        """QSort pivoting for lst[lo:hi] with a randomized pivot
        Returns the pivot index. lst[lo:p] <= lst[p] < lst[p+1:hi]"""
        p = random.randrange(lo,hi)
        pivot_val = lst[p]
        swap(lst,p,hi-1)
        storeIndex = lo
        for i in range(lo, hi-1):
            if self.comp(lst[i], pivot_val) <= 0: 
                swap(lst, i, storeIndex)
                storeIndex = storeIndex + 1
        swap(lst, storeIndex, hi-1)
        return storeIndex
        
    def q_sort(self,lst,lo,hi,comp):
        """full QSort algorithm for the internal state"""
        if lo >= hi-1: return
        p = self.partition(lst,lo,hi,comp)
        self.q_sort(lst,lo,p,comp)
        self.q_sort(lst,p,hi,comp)
    
    def sort(self,lst):
        self.q_sort(lst,0,len(lst),self.comp)

class MergeSorter(Sorter):
    """Recursive, non-in-place implementation"""
    def __init__(self, comp):
        Sorter.__init__(self,comp)
        self.name = 'MergeSort'

    def merge(self,lst,lo,mid,hi,comp):
        """Given two sorted segments [lo:mid] and [mid:hi], 
        merge them into a big, sorted list"""
        cpylst = lst[lo:mid]
        ind1 = 0
        ind2 = mid
        real_ind = lo
        while ind1<mid-lo and ind2<hi:
            if comp(cpylst[ind1],lst[ind2]) < 0:
                lst[real_ind] = cpylst[ind1]
                ind1+=1
            else:
                lst[real_ind] = lst[ind2]
                ind2+=1
            real_ind+=1
        if ind2==hi: #if you run out of the second segment first
            while ind1 < len(cpylst):
                lst[real_ind] = cpylst[ind1]
                ind1+=1
                real_ind+=1
    
    def m_sort(self,lst,lo,hi,comp):
        if hi-lo <= 1: return lst
        mid = lo + (hi-lo)//2
        self.m_sort(lst,lo,mid,comp)
        self.m_sort(lst,mid,hi,comp)
        self.merge(lst,lo,mid,hi,comp)
    
    def sort(self,lst):
        self.m_sort(lst,0,len(lst),self.comp)

class InsertionSorter(Sorter):
    """Simple insertion sorting algo"""
    def __init__(self, comp):
        Sorter.__init__(self,comp)
        self.name = 'InsertionSort'

    def in_sort(self,lst,lo,hi,comp):
        for ind in range(lo,hi):
            n = lo
            lim = hi-(ind-lo)-1
            while n<lim:
                if comp(lst[n],lst[n+1]) > 0:
                    swap(lst,n,n+1)
                n+=1
    
    def sort(self,lst):
        self.in_sort(lst,0,len(lst),self.comp)

class BubbleSorter(Sorter):
    def __init__(self, comp):
        Sorter.__init__(self,comp)
        self.name = 'BubbleSort'

    def bub_sort(self,lst,lo,hi,comp):
        for ind in range(lo,hi):
            n = hi-1
            while n > ind:
                if comp(lst[n-1],lst[n]) > 0:
                    swap(lst,n-1,n)
                n-=1
    
    def sort(self,lst):
        self.bub_sort(lst,0,len(lst),self.comp)

class SelectionSorter(Sorter):
    def __init__(self, comp):
        Sorter.__init__(self,comp)
        self.name = 'Selection Sort'

    def sel_sort(self,lst,lo,hi,comp):
        for ind in range(lo,hi):
            min_so_far = ind
            cmp_ind = ind+1
            while cmp_ind<hi:
                if self.comp(lst[cmp_ind],lst[min_so_far]) < 0:
                    min_so_far = cmp_ind
                cmp_ind+=1
            swap(lst,min_so_far,ind)
    
    def sort(self,lst):
        self.sel_sort(lst,0,len(lst),self.comp)

class BogoSorter(Sorter):
    def __init__(self, comp):
        Sorter.__init__(self,comp)
        self.name = 'BogoSort'

    def bogosort(self,lst,lo,hi,comp):
        start = time.time()
        while not is_in_order(lst,lo,hi,comp):
            new_list = lst[lo:hi]
            lst[lo:hi] = random.sample(new_list,len(new_list))
            if time.time()-start>100: raise TimeoutException
    
    def sort(self,lst):
        self.bogosort(lst,0,len(lst),self.comp)

class HeapSorter(Sorter):
    class Heap(object):
        """implementation of a min-heap"""
        def __init__(self, comp):
            self.heap = []
            self.comp = comp
        
        def bub_up(self):
            """bubbles up the last element"""
            h = self.heap
            ind = len(h)-1
            parent = (ind-1)//2
            while ind>0 and self.comp(h[parent],h[ind])>0:
                swap(h,ind,parent)
                ind = parent
                parent = (ind-1)//2
        
        def bub_down(self):
            """bubbles down the first element"""
            h = self.heap
            ind = 0
            placed = False
            while not placed and 2*ind+1<len(h):
                smaller_child = 2*ind+1
                if 2*ind+2<len(h) and self.comp(h[2*ind+1],h[2*ind+2])>0:
                    smaller_child = 2*ind+2
                if self.comp(h[ind],h[smaller_child])>0:
                    swap(h,ind,smaller_child)
                    ind = smaller_child
                else: placed = True
        
        def add(self,elt):
            self.heap.append(elt)
            self.bub_up()
        
        def poll(self):
            h = self.heap
            length = len(h)
            if length<1: raise Exception
            save = h[0]
            h[0] = h[length-1]
            del h[length-1]
            self.bub_down()
            return save

    def __init__(self, comp):
        Sorter.__init__(self,comp)
        self.name = 'HeapSort'

    def heapsort(self,lst,lo,hi,comp):
        h = HeapSorter.Heap(comp)
        for ind in range(lo,hi):
            h.add(lst[ind])
        for ind in range(lo,hi):
            lst[ind] = h.poll()

    def sort(self,lst):
        self.heapsort(lst,0,len(lst),self.comp)

arr = [#BogoSorter(cmp), 
        BubbleSorter(cmp), SelectionSorter(cmp),
        InsertionSorter(cmp), HeapSorter(cmp), MergeSorter(cmp),
        QuickSorter(cmp)]
        
print('Sorting lists of size {}, taken the average of {} trials'.format(size,trials))
for ob in arr:
    print(ob)

