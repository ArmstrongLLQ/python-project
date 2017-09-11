#导入模块
#collections.namedtuple() 函数实际上是一个返回Python中标准元组类型子类的一个工厂方法。
#你需要传递一个类型名和你需要的字段给它，然后它就会返回一个类，你可以初始化这个类，
#为你定义的字段传递值等。 详情参见官方文档。
import sys
import os
import _io
from collections import namedtuple
from PIL import Image

#设计一个Nude类,用于表示像素
class Nude(object):
    Skin = namedtuple("Skin", "id skin region x y")
    def __init__(self, path_or_image):
        #若path_or_image为Image.Image类型的实例(图片)，直接赋值
        if isinstance(path_or_image, Image.Image):
            self.image = path_or_image
        #若path_or_imag为str类型的实例(路径)，则打开图片
        elif isinstance(path_or_image, str):
            self.image = Image.open(path_or_image)
        #接下来的self.image就是一个Image对象
        #获得图片所有颜色通道,getbands是Image库中的函数
        bands = self.image.getbands()
        #判断是否为单通道图片（也称灰度图），是则将灰度图转化为RGB图
        if len(bands) == 1:  #如果是灰度图，拷贝一份转换成RGB图
            #新建相同大小的RGB图样
            new_img = Image.new("RGB", self.image.size)
            #拷贝灰度图self.image到RGB图 new_img.paste（PIL自动进行颜色通道转换）
            new_img.paste(self.image)
            f = self.image.filename
            # 替换self.image
            self.image = new_img
            self.image.filename = f

        #存储对应图像所有像素的全部skin对象，即将图像中的每个像素点转化成skin对象(列表)
        self.skin_map = []
        #检测到的皮肤区域，元素的索引即为皮肤区域号，元素都是一些由像素转化成的skin对象(列表)
        self.detected_regions = []
        #元素都是包含一些int对象（区域号）的列表
        #这些元素中的区域号代表的区域都是待合并的区域
        self.merge_regions = []   #每个元素是一个列表，每个元素包含的元素都是待合并的对象
        #整合后的皮肤区域，元素的索引即为皮肤区域号，元素都是一些包含skin对象的列表
        self.skin_regions = []    #self.merge_regions列表中每个小列表合并后形成的新列表
        #最近合并的两个皮肤的区域号，初始化为-1
        self.last_from, self.last_to = -1, -1
        #色情图片判断结果
        self.result = None
        #处理器得到的信息
        self.message = None
        #图像的宽和高
        self.width, self.height = self.image.size  #size包含像素宽和高的元组
        #图片的总像素
        self.total_pixels = self.width * self.height

    #涉及到效率问题，越大的图片消耗的资源与时间也越大，因此有时候需要对图片进行缩小
    #所以首先写图片缩小方法
    def resize(self, maxwidth=1000, maxheight=1000):  #这段代码有改进空间
        '''
        基于最大宽高比按比例重设图片大小
        注意：这可能影响检测算法的结果

        如果没有变化返回0
        原宽度大于 maxwidth 返回1
        原高度大于 maxheight 返回2
        原宽高大于 maxwidth，maxheight 返回3

        maxwidth - 图片最大宽度
        maxheight - 图片最大宽度
        传递参数时都可以设置成 False 
        '''
        #存储返回值
        ret = 0
        if maxwidth:
            if self.width > maxwidth:
                wpercent = (maxwidth / self.width)   #对应的缩小比例为最大宽度除以像素
                hsize = int(self.height * wpercent)  #缩小比例乘以图片的像素高，得到缩小后的图片高
                fname = self.image.filename          #用于记录并存储新文件，即缩小后的文件
                #Image.LANCZOS是重采样率滤波器，用于抗锯齿
                self.image = self.image.resize((maxwidth, hsize), Image.LANCZOS)
                self.image.filename = fname
                self.width, self.height = self.image.size  #同样是根据图片的大小生成宽和高的元组
                self.total_pixels = self.width * self.height
                ret += 1
        if maxheight:  #思路与上同理，宽高等比例缩小，并修改最终像素
            if self.height > maxheight:
                hpercent = (maxheight / float(self.height))
                wsize = int((float(self.width) * float(hpercent)))
                fname = self.image.filename
                self.image = self.image.resize((wsize, maxheight), Image.LANCZOS)
                self.image.filename = fname
                self.width, self.height = self.image.size
                self.total_pixels = self.width * self.height
                ret += 2
            return ret
    #解析方法
    def parser(self):
        #如果已有结果，返回本对象
        if self.result is not None:
            return self
        #获得图片所有像素数据
        pixels = self.image.load()  #每个像素点都是列表对象，可以切片得到RGB值
        #接着，遍历每个像素，为每个像素创建对应的 Skin 对象
        for y in range(self.height):
            for x in range(self.width):
                #得到像素的RGB三个通道的值
                #[x, y]是[(x, y)]的简便方法
                r = pixels[x, y][0] #red
                g = pixels[x, y][1] #green
                b = pixels[x, y][2] #blue
                #判断当前像素是否为肤色像素, _classify_skin()方法判断监测像素颜色是否为肤色
                isSkin = True if self._classify_skin(r, g, b) else False
                #给每一个像素分配唯一 id值（1,2,3...height*width）
                #注意x，y的值从零开始
                _id = x + y * self.width + 1
                #为每一个像素创建一个对应的Skin对象，并添加到self.skin_map中
                self.skin_map.append(self.Skin(_id, isSkin, None, x, y))
                #若当前像素不是肤色像素，那么不需要进行处理
                if not isSkin:
                    continue
                #设左上角为原点，相邻像素为符号*，当前像素为符号^，那么相互位置关系通常如下
                #***
                #*^
                #存在相邻像素的列表，存放顺序由大到小，顺序改变有影响
                #注意_id是从1开始的，对应的索引号即为_id-1
                check_index = [_id - 2, #当前像素左方的像素
                               _id - self.width - 2, #当前像素左上方的像素
                               _id - self.width - 1,  #当前像素上方的像素
                               _id - self.width]#当前像素右上方的像素
                #用来记录像素中肤色像素所在的区域号，初始化为-1
                region = -1
                #遍历每一个相邻像素的索引
                for index in check_index:
                    #尝试索引相邻像素的Skin对象，没有则跳出循环
                    try:
                        self.skin_map[index]
                    except IndexError:
                        break
                    #相邻像素若为肤色像素：
                    if self.skin_map[index].skin:
                        #若相邻像素与当前像素的region均为有效值,
                        #且二者不同，且尚未添加相同的合并任务
                        if (self.skin_map[index].region != None and
                            region != None and region != -1 and
                            self.skin_map[index].region != region and
                            self.last_from != region and
                            self.last_to != self.skin_map[index].region):
                            #那么就添加这两个区域的合并任务
                            self._add_merge(region, self.skin_map[index].region)
                        #记录此相邻像素所在的区域号
                        region = self.skin_map[index].region
                #遍历完所有相邻像素后，若region仍等于-1，说明所有的相邻像素不是肤色像素
                if region == -1:
                    #更改属性为新的区域号，注意元组是不可变类型，不能直接更改其属性
                    _skin = self.skin_map[_id - 1]._replace(region=len(self.detected_regions))
                    self.skin_map[_id - 1] = _skin
                    #将此肤色像素所在区域创建为新区域
                    self.detectd_regions.append(self.skin_map[_id-1])
                elif region != None:
                    #将此像素的区域号更改为与相邻像素相同
                    _skin = self.skin_map[_id - 1]._replace(region=region)
                    self.skin_map[_id - 1] = _skin
                    #然后向这个像素列表中添加此像素
                    self.detectd_regions[region].append(self.skin_map[_id - 1])
        #遍历完所有像素之后，图片的皮肤区域划分初步完成了
        # 只是在变量 self.merge_regions 中还有一些连通的皮肤区域号，它们需要合并
        # 合并之后就可以进行色情图片判定了

        #完成所有区域的合并任务，合并整理后的区域存储到self.skin_region
        self._merge(self.detected_regions, self.merge_regions)
        #分析皮肤区域，得到判定结果
        self._analyse_regions()
        return self

    #基于像素的肤色检测技术
    def _classify_skin(self, r, g, b):
        #根据RGB值判定
        rgb_classifier = r > 95 and \
            g > 40 and g < 100 and \
            b > 20 and \
            max([r, g, b]) - min([r, g, b]) > 15 and \
            abs(r - g) > 15 and \
            r > g and \
            r > b
        #根据处理后的RGB值判定
        nr, ng, nb = self._to_normalized(r, g, b)
        norm_rgb_classifier = nr / ng > 1.185 and \
            float(r * b) / ((r + g + b) **2) > 0.107 and \
            float(r * g) / ((r + g + b) ** 2) > 0.112

        #HSV颜色模式下的判定
        h, s, v = self._to_hsv(r, g, b)
        hsv_classfier = h > 0 and \
            h < 35 and \
            s > 0.23 and \
            s < 0.68

        #YCbCr颜色模式下的判定
        y, cb, cr = self._to_ycbcr(r, g, b)
        ycbcr_classifier = 9.75 <= cb <= 142.5 and 134 <= 176

        #效果不是很好，可以修改公式
        # return rgb_classifier or norm_rgb_classifier or hsv_classifier or ycbcr_classifier
        return ycbcr_classifier


    #接下来三个方法实现对颜色模式的转换
    def _to_normalized(self, r, g, b):
        if r == 0:
            r = 0.0001
        if g == 0:
            g = 0.0001
        if b == 0:
            b = 0.0001
        _sum = float(r + g + b)
        return [r / _sum, g / _sum, b / _sum]

    def _to_ycbcr(self, r, g, b):
        if r == 0:
            r = 0.0001
        if g == 0:
            g = 0.0001
        if b == 0:
            b = 0.0001
        _sum = float(r + g + b)
        return [r / _sum, g / _sum, b / _sum]

    def _to_hsv(self, r, g, b):
        h = 0
        _sum = float(r + g + b)
        _max = float(max([r, g, b]))
        _min = float(min([r, g, b]))
        diff = float(_max - _min)
        if _sum == 0:
            _sum = 0.0001

        if _max == r:
            if diff == 0:
                h = sys.maxsize
            else:
                h = (g - b) / diff
        elif _max == g:
            h = 2 + ((g - r) / diff)
        else:
            h = 4 + ((r - g) / diff)

        h *= 60
        if h < 0:
            h += 360

        return [h, 1.0 - (3.0 * (_min / _sum)), (1.0 / 3.0) * _max]

    #这个方法主要是对self.merge_regions操作，而self.merge_regions的元素
    #都是包含一些int对象（区域号）的列表，每个列表中的区域需要进行合并成一个区域
    def _add_merge(self, _from, _to):
        #两个区域号，赋值给类属性
        self.last_from = _from
        self.last_to = _to

        #记录self.merge_regions的某个索引值， 初始化为-1
        from_index = -1
        #记录self.merge_regions的某个索引值， 初始化为-1
        to_index = -1

        #遍历每个self.merge_region的元素,索引位置和对应值可以使用 enumerate() 函数同时得到
        for index, region in enumerate(self.merge_regions):
            #遍历元素中的某个区域号
            for r_index in region:
                if r_index == _from:
                    from_index = index
                if r_index == _to:
                    to_index = index

        #若两个区域都存在于self.merge_regions中
        if from_index != -1 and to_index != -1:
            #如果这两个区域号分别存在于两个列表中
            #那么合并这两个列表
            if from_index != to_index:
                self.merge_regions[from_index].extend(self.merge_regions[to_index])
                del(self.merge_regions[to_index])
            return

    #self._merge() 方法则是将 self.merge_regions 中的元素中的区域号所代表的区域合并，得到新的皮肤区域列表
    def _merge(self, detected_regions, merge_regions):
        #新建列表new_detected_regions
        #其元素讲是一些代表像素的Skin对象的列表
        #new_dected_regions的元素即代表皮肤区域，元素索引即为区域号
        new_detected_regions = []
        #将merge_regions中的元素代表的所有区域合并
        for index, region in enumerate(merge_regions):
            try:
                new_detected_regions[index]
            except IndexError:
                new_detected_regions.append([])
            for r_index in region:
                new_detected_regions[index].extend(detected_regions[r_index])
                detected_regions[r_index] = []

        #添加剩下的其他皮肤区域到new_detected_regions
        for region in detected_regions:
            if len(region) > 0:
                new_detected_regions.append(region)

        #清理 new_dected_regions
        self._clear_regions(new_detected_regions)
        #添加剩下的其余皮肤到new_detected_regions
        for region in detected_regions:
            if len(region) > 0:
                new_detected_regions.append(region)
        #清理new_detected_regions
        self._clear_regions(new_detected_regions)

    # 皮肤区域清理函数
    # 只保存像素数大于指定数量的皮肤区域
    def _clear_regions(self, detected_regions):
        for region in detected_regions:
            if len(region) > 30:
                self.skin_regions.append(region)

    #分析区域
    def _analyse_regions(self):
        #如果皮肤区域小于3个，不是色情
        if len(self.skin_regions) < 3:
            self.message = "Less than 3 skin regions ({_skin_regions_size})".format(
                _skin_regions_size=len(self.skin_regions))
            self.result = False
            return self.result
        #为皮肤区域排序
        self.skin_regions = sorted(self.skin_regions, key=lambda s: len(s), reverse = True)
        #计算皮肤总像素数
        total_skin = float(sum([len(skin_region) for skin_region in self.skin_regions]))
        #如果皮肤区域与整个图像的壁纸小于15%，那么不是色情图片
        if total_skin / self.total_pixels * 100 < 15:
            self.message = "Total skin percentage lower than 15 ({:.2f})".format(total_skin / self.total_pixels * 100)
            self.result = False
            return self.result

            # 如果最大皮肤区域小于总皮肤面积的 45%，不是色情图片
        if len(self.skin_regions[0]) / total_skin * 100 < 45:
            self.message = "The biggest region contains less than 45 ({:.2f})".format(
                len(self.skin_regions[0]) / total_skin * 100)
            self.result = False
            return self.result

            # 皮肤区域数量超过 60个，不是色情图片
        if len(self.skin_regions) > 60:
            self.message = "More than 60 skin regions ({})".format(len(self.skin_regions))
            self.result = False
            return self.result

            # 其它情况为色情图片
        self.message = "Nude!!"
        self.result = True
        return self.result

    #对分析的信息进行组合
    def inspect(self):
        _image = '{} {} {}×{}'.format(self.image.filename, self.image.format, self.width, self.height)
        return "{_image}: result={_result} message='{_message}'".format(_image=_image, _result=self.result,_message=self.message)


    def inspect(self):
        _image = '{} {} {}×{}'.format(self.image.filename, self.image.format, self.width, self.height)
        return "{_image}: result={_result} message='{_message}'".format(_image=_image, _result=self.result, _message=self.message)


    # 将在源文件目录生成图片文件，将皮肤区域可视化
    def showSkinRegions(self):
        # 未得出结果时方法返回
        if self.result is None:
            return
        # 皮肤像素的 ID 的集合
        skinIdSet = set()
        # 将原图做一份拷贝
        simage = self.image
        # 加载数据
        simageData = simage.load()

        # 将皮肤像素的 id 存入 skinIdSet
        for sr in self.skin_regions:
            for pixel in sr:
                skinIdSet.add(pixel.id)
        # 将图像中的皮肤像素设为白色，其余设为黑色
        for pixel in self.skin_map:
            if pixel.id not in skinIdSet:
                simageData[pixel.x, pixel.y] = 0, 0, 0
            else:
                simageData[pixel.x, pixel.y] = 255, 255, 255
        # 源文件绝对路径
        filePath = os.path.abspath(self.image.filename)
        # 源文件所在目录
        fileDirectory = os.path.dirname(filePath) + '/'
        # 源文件的完整文件名
        fileFullName = os.path.basename(filePath)
        # 分离源文件的完整文件名得到文件名和扩展名
        fileName, fileExtName = os.path.splitext(fileFullName)
        # 保存图片
        simage.save('{}{}_{}{}'.format(fileDirectory, fileName,'Nude' if self.result else 'Normal', fileExtName))
    # Nude类结束

if __name__ == "__main__":
    fname = "timg.jpg"
    if os.path.isfile(fname):
        n = Nude(fname)
        n.resize(maxheight=800, maxwidth=600)
        n.parser()
        n.showSkinRegions()
        print(n.result, n.inspect())
    else:
        print(fname, "is not a file")