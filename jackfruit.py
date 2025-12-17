import wx   # type: ignore
from PIL import Image, ImageEnhance, ImageFilter, ImageOps  # type: ignore


# Define the frame class
class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        
        # Image path
        self.img_path = "sample.jpg"  

        # Load image
        self.image = wx.Image(self.img_path, wx.BITMAP_TYPE_ANY)
        self.curr_img = self.image.Copy()

        h , w = self.image.GetHeight(), self.image.GetWidth()

        super().__init__(parent, title=title, size=(w, h + 200))
        self.panel = wx.Panel(self)
       

        # Show image
        bitmap = wx.Bitmap(self.image)
        wx.StaticBitmap(self.panel, -1, bitmap, (0, 0))

        # Dropdown for operations
        self.choices = ['Original','Grayscale', 'Sepia', 'Invert', 'Blur', 'Sharpen', 'Edge Enhance', 'Emboss', 'Posterize', 'Solarize', 'Increase Brightness', 'Increase Contrast']
        self.choice = wx.Choice(self.panel, choices=self.choices, pos=( 40, h + 40), size = (100,30))
        self.choice.SetSelection(0)  # default selection

        # Button to apply operation
        self.apply = wx.Button(self.panel, label='Apply', pos=(40, h + 100), size = (100,30))
        self.apply.Bind(wx.EVT_BUTTON, self.on_apply)
        
        # Top 5 colors button
        self.show_colors = wx.ToggleButton(self.panel, label='Show Top 5 Colors', pos=(200, h + 40), size = (150,30))
        self.show_colors.Bind(wx.EVT_TOGGLEBUTTON, self.on_show_colors)
        
        # Center and show the frame
        self.Centre()
        self.Show()

    # On_apply event handler
    def on_apply(self, event):
        sel = self.choice.GetString(self.choice.GetSelection())
        self.curr_img = Image.open(self.img_path).convert('RGBA')
        self.curr_img = self.apply_named_filter(self.curr_img, sel)
        if self.curr_img:
            wx_image = wx.Image(self.curr_img.size[0], self.curr_img.size[1])
            wx_image.SetData(self.curr_img.convert('RGB').tobytes())
            bitmap = wx.Bitmap(wx_image)
            static_bitmap = wx.StaticBitmap(self.panel, -1, bitmap, (0, 0))
            self.panel.Refresh()
        
    # Apply_named_filter to PIL image
    def apply_named_filter(self, pil_img, filter_name):
        if pil_img is None:
            return None
        img = pil_img
        name = filter_name.lower()
        if 'original' in name:
            return img
        if 'grayscale' in name:
            return ImageOps.grayscale(img).convert('RGBA')
        if 'sepia' in name:
            base = img.convert('RGB')
            sep = Image.new('RGB', base.size)
            pixels = base.load()
            sep_pixels = sep.load()
            for x in range(base.size[0]):
                for y in range(base.size[1]):
                    r, g, b = pixels[x, y]
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    sep_pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))
            out = Image.blend(base, sep, 1.0)
            return out.convert('RGBA')
        if 'invert' in name:
            return ImageOps.invert(img.convert('RGB')).convert('RGBA')
        if 'blur' in name:
            return img.filter(ImageFilter.GaussianBlur(radius=5))
        if 'sharpen' in name:
            return img.filter(ImageFilter.UnsharpMask(radius=2, percent=50, threshold=3))
        if 'edge enhance' in name:
            return img.filter(ImageFilter.EDGE_ENHANCE)
        if 'emboss' in name:
            return img.filter(ImageFilter.EMBOSS)
        if 'posterize' in name:
            return ImageOps.posterize(img.convert('RGB'), bits=3).convert('RGBA')
        if 'solarize' in name:
            return ImageOps.solarize(img.convert('RGB'), threshold=128).convert('RGBA')
        if 'brightness' in name:
            return ImageEnhance.Brightness(img).enhance(1.3)
        if 'contrast' in name:
            return ImageEnhance.Contrast(img).enhance(1.3)
        return img
    
    # Get_top_colors method
    def get_top_colors(self, pil_img, n=5):
        # Accept either a PIL.Image or a wx.Image
        # If it's a wx.Image, convert to PIL.Image
        if hasattr(pil_img, 'GetData') and hasattr(pil_img, 'GetWidth'):
            w, h = pil_img.GetWidth(), pil_img.GetHeight()
            if pil_img.HasAlpha():
                rgb_data = pil_img.GetData()  # RGB bytes
                alpha_data = pil_img.GetAlpha()  # alpha bytes
                rgb = Image.frombytes('RGB', (w, h), rgb_data)
                a = Image.frombytes('L', (w, h), alpha_data)
                img = rgb.convert('RGBA')
                img.putalpha(a)
            else:
                rgb_data = pil_img.GetData()
                img = Image.frombytes('RGB', (w, h), rgb_data)
        else:
            # Assume it's already a PIL image
            if pil_img.mode not in ('RGB', 'RGBA'):
                img = pil_img.convert('RGB')
            else:
                img = pil_img.convert('RGB')
        w, h = img.size
        max_dim = 200
        if max(w, h) > max_dim:
            try:
                res = Image.Resampling.LANCZOS
            except AttributeError:
                res = Image.LANCZOS
            img = img.resize((int(w * max_dim / max(w, h)), int(h * max_dim / max(w, h))), resample=res)
        quantized = img.quantize(colors=n, method=Image.MEDIANCUT)
        colors = quantized.getcolors()
        if not colors:
            return []
        palette = quantized.getpalette()

        def index_to_rgb(i):
            base = i * 3
            return tuple(palette[base:base + 3])

        color_counts = [(cnt, index_to_rgb(idx)) for (cnt, idx) in colors]
        color_counts.sort(reverse=True, key=lambda t: t[0])
        return [rgb for cnt, rgb in color_counts[:n]]

    # On_show_colors event handler
    def on_show_colors(self, evt):
        if self.show_colors.GetValue():
            if self.curr_img is None:
                wx.MessageBox('Open an image first', 'Info', wx.ICON_INFORMATION)
                return
            colors = self.get_top_colors(self.curr_img, n=5)
            frame = PaletteFrame(self, colors)
            frame.Show()
        
        else:
            # Close the palette frame if it exists
            for child in self.GetChildren():
                if isinstance(child, PaletteFrame):
                    child.Close()


class PaletteFrame(wx.Frame):
    def __init__(self, parent, colors, size=None):
        # Compute a size that fits the color swatches and, if possible, match
        # the height to the parent's image height (so it visually lines up)
        super().__init__(parent, title='Palette - Top Colors', size=size or wx.DefaultSize)
        panel = wx.Panel(self)

        # Arrange the colors vertically (one per row) so they visually match the
        # image height if needed.
        sizer = wx.BoxSizer(wx.VERTICAL)
        swatch_size = 60
        label_max_width = 0
        rows = []
        for rgb in colors:
            hex_code = '#%02x%02x%02x' % rgb
            row = wx.Panel(panel)
            row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            col_panel = wx.Panel(row, size=(swatch_size, swatch_size))
            col_panel.SetBackgroundColour(hex_code)
            label = wx.StaticText(row, label=hex_code)
            # Track widest label to calculate frame width later
            label_best = label.GetBestSize()
            if label_best.GetWidth() > label_max_width:
                label_max_width = label_best.GetWidth()
            row_sizer.Add(col_panel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
            row_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 6)
            row.SetSizer(row_sizer)
            sizer.Add(row, 0, wx.EXPAND | wx.ALL, 2)
            rows.append(row)
        # Add all rows to the main sizer
        panel.SetSizer(sizer)

        # Let sizer compute the minimal size
        sizer.Fit(self)
        self.Layout()

        # Optionally set the height to match the parent image height, if available
        desired_height = self.GetSize().GetHeight()
        desired_width = self.GetSize().GetWidth()

        # Calculate width based on swatch size and the widest label (plus padding)
        desired_width = max(desired_width, swatch_size + label_max_width + 40)
        # Set the size and center the palette frame
        self.SetSize((desired_width, desired_height))
        self.Center()



app = wx.App()
frame = MainFrame(None, title="wx.Image Processing")
app.MainLoop()    

