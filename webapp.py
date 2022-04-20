import justpy as jp
import model


class TabsPills(jp.Div):
    item_classes = 'flex-shrink m-1'
    item_classes_selected = 'flex-shrink m-1'
    wrapper_style = 'display: flex; flex-wrap: wrap; width: 100%;'\
                    'height: 100%;  align-items: center;'\
                    'justify-content: center; background-color: #fff;'\
                    'font-family: \'Poppins\', sans-serif;'

    def __init__(self, **kwargs):

        self.tabs = []  # list of {'id': id, 'label': label, 'content': content}
        self.value = None  # The value of the tabs component is the id of the selected tab
        self.content_height = 600
        self.last_rendered_value = None
        self.animation = False
        self.animation_style = 'animate__fadeIn'
        self.animation_speed = 'faster'  # '' | 'slow' | 'slower' | 'fast'  | 'faster'
        self.text_color = 'black'
        self.hover_bg = 'gray-100'
        self.selected_text_color = 'pink-400'
        self.tab_list_bg = 'white'
        self.border = ''
        
        super().__init__(**kwargs)

        self.tab_label_classes = f'cursor-pointer inline-block rounded-lg m-3 py-1 px-3 text-{self.text_color} font-semibold hover:bg-{self.hover_bg}'
        self.tab_label_classes_selected = f'cursor-pointer inline-block rounded-lg m-3 py-1 px-3 text-{self.selected_text_color} font-semibold'
        self.tab_list = jp.Ul(classes=f'flex overflow-x-auto text-center text-sm md:text-md bg-{self.tab_list_bg} items-center justify-between px-8 {self.border}', a=self)
        self.content_div = jp.Div(a=self)
        self.delete_list = []


    def __setattr__(self, key, value):
        if key == 'value':
            try:
                self.previous_value = self.value
            except:
                pass
        self.__dict__[key] = value

    def add_tab(self, id, label, content):
        self.tabs.append({'id': id, 'label': label, 'content': content})
        if not self.value:
            self.value = id

    def get_tab_by_id(self, id):
        for tab in self.tabs:
            if tab['id'] == id:
                return tab
        return None

    def set_content_div(self, tab):
        self.content_div.add(tab['content'])
        self.content_div.set_classes('relative overflow-hidden')
        self.content_div.style = f'height: {self.content_height}px;'

    def set_content_animate(self, tab):
        self.wrapper_div_classes = self.animation_speed  # Component in this will be centered
        if self.previous_value:
            self.wrapper_div = jp.Div(classes=self.wrapper_div_classes, animation=self.animation_style, temp=True,
                                   style=f'{self.wrapper_style} z-index: 50;', a=self.content_div)
            self.wrapper_div.add(tab['content'])
            self.wrapper_div = jp.Div(classes=self.wrapper_div_classes, animation=self.animation_style, temp=True,
                                   style=f'{self.wrapper_style} z-index: 0;', a=self.content_div)
            self.wrapper_div.add(self.get_tab_by_id(self.previous_value)['content'])
        else:
            self.wrapper_div = jp.Div(classes=self.wrapper_div_classes, temp=True, a=self.content_div,
                                   style=self.wrapper_style)
            self.wrapper_div.add(tab['content'])
        
        self.content_div.set_classes('relative overflow-hidden')
        self.content_div.style = f'height: {self.content_height}px;'

    def model_update(self):
        val = self.model[0].data[self.model[1]]
        if self.get_tab_by_id(val):
            self.value = val

    def delete(self):
        for c in self.delete_list:
            c.delete_flag = True
            c.delete()
            c.needs_deletion = False

        if self.delete_flag:
            for tab in self.tabs:
                tab['content'].delete()
                tab['content'] = None
        super().delete()

    @staticmethod
    async def tab_click(self, msg):
        if self.tabs.value != self.tab_id:
            previous_tab = self.tabs.value
            self.tabs.value = self.tab_id
            if hasattr(self.tabs, 'model'):
                self.tabs.model[0].data[self.tabs.model[1]] = self.tabs.value
            # Run change if it exists
            if self.tabs.has_event_function('change'):
                msg.previous_tab = previous_tab
                msg.new_tab = self.tabs.value
                msg.id = self.tabs.id
                msg.value = self.tabs.value
                msg.class_name = self.tabs.__class__.__name__
                return await self.tabs.run_event_function('change', msg)
        else:
            return True  # No need to update page

    def convert_object_to_dict(self):
        if hasattr(self, 'model'):
            self.model_update()
        self.set_classes('flex flex-col')
        self.tab_list.delete_components()
        self.content_div.components = []
        for tab in self.tabs:
            if tab['id'] != self.value:
                tab_li = jp.Li(a=self.tab_list, classes=self.item_classes)
                li_item = jp.A(text=tab['label'], classes=self.tab_label_classes, a=tab_li, delete_flag=False)
                self.delete_list.append(li_item)
            else:
                tab_li = jp.Li(a=self.tab_list, classes=self.item_classes_selected)
                li_item = jp.A(text=tab['label'], classes=self.tab_label_classes_selected, a=tab_li, delete_flag=False)
                self.delete_list.append(li_item)
                if self.animation and (self.value != self.last_rendered_value):
                    self.set_content_animate(tab)
                else:
                    self.set_content_div(tab)
            li_item.tab_id = tab['id']
            li_item.tabs = self
            li_item.on('click', self.tab_click)
        self.last_rendered_value = self.value
        d = super().convert_object_to_dict()

        return d
    

class Section():
    def __init__(self, name: str, link) -> None:
        self.name = name
        self.link = link
        

def shop_section(section_div):
    products_div = jp.Div(a=section_div, style='width: 100%; height: 100%;')
    jp.Br(a=products_div)
    
    category_bar = TabsPills(   # Navigation bar for categories
        a=products_div, 
        classes='w-full', 
        style='font-family: \'Poppins\'',
        animation=False, 
        content_height='100%',
    )
    for category in ['Todos los productos', 'Prendas Superiores',
                    'Pantalones', 'Faldas', 'Accesorios',
                    'Maquillaje']:
        products_div = jp.Div(classes='flex flex-wrap content-start '\
                                   'place-content-around justify-center '\
                                   'relative overflow-y-auto')
        # Gets available products
        result_proxy = model.get_available_products()
        for row in result_proxy:
            if (category=='Todos los productos' 
                or (category!='Todos los productos' 
                    and row.category==category)):
                # Container for individual product layout
                product_layout = jp.Div(a=products_div, classes='flex '\
                                        'flex-col m-4 p-4 inline-block '\
                                        'items-center font-semibold '\
                                        'rounded-lg hover:bg-gray-100',
                )
                    
                # Adds components to product layout
                image = row.images.split('-')[0]
                jp.Img(
                    a=product_layout,
                    src=f'/static/media/{image}', 
                    style='height: 300px;', 
                    classes='overflow-hidden'
                )
                jp.P(a=product_layout, text=row.name.upper(),
                    classes='text-pink-400 mt-3')
                jp.P(a=product_layout, text=f'${row.price}')
                product_layout.product = model.Product(
                product_id=row.product_id,
                name=row.name,
                price=row.price,
                category=row.category,
                description=row.description,
                images=row.images,
                colors=row.colors,
                sizes=row.sizes,
                availability=row.availability,
            )
        # Adds tab for category to category navigation bar
        category_bar.add_tab(f'id{category}', f'{category}', products_div)

def about_section(section_div):
    pass

def consult_order_section(section_div):
    pass

def instructions_section(section_div):
    pass

def cart_section(section_div):
    pass

def admin_section(section_div):
    pass
    
sections = [
    Section('Productos', shop_section),
    Section('Acerca de Buhi', about_section),
    Section('Consultar Orden', consult_order_section),
    Section('Ayuda', instructions_section),
    Section('Carrito', cart_section),
    Section('Admin', admin_section),
]

cart = model.Cart()

def app():
    wp = jp.WebPage(template_file='tailwindui.html')
    # Adds links to the fonts that will be used 
    wp.head_html = '<link rel="preconnect" href="https://fonts.googleapis.com">' \
                   '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' \
                   '<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,600;0,700;1,700&display=swap" rel="stylesheet">'
    wp.css = "body { font-family: 'Poppins', sans-serif; }"
    wp_div = jp.Div(classes='flex flex-col', a=wp)  # Main container
    
    title_header = jp.Div(a=wp_div, classes='w-full flex flex-shrink '\
                          'bg-pink-400 text-white text-6xl font-bold '\
                          'justify-center items-center', 
                          style='font-family: \'Poppins\', sans-serif;')
    title_header.add(jp.Img(src='/static/media/logo.png', classes='h-12 mx-3'))
    title_header.add(jp.Strong(text='Buhi Store', classes='my-2'))
    
    nav_bar = TabsPills(    # Main navigation bar linking to sections
        a=wp_div, 
        classes='w-full',
        style='font-family: \'Poppins\', sans-serif;',
        animation=False, 
        content_height='100%',
        hover_bg='gray-900',
        text_color='white',
        tab_list_bg='black',
    )
    for section in sections:
        section_div = jp.Div(style=TabsPills.wrapper_style)
        section.link(section_div)   # Adds content corresponding to section to div
        nav_bar.add_tab(    # Adds tab for section to main navigation bar
            f'id{section.name}',
            f'{section.name.upper()}',
            section_div,
        ) 
        
    return wp

jp.justpy(app)