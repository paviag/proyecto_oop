from functools import wraps
from typing import Any

import justpy as jp

import model
import database as db
import file_handling as file

button_classes = 'flex items-center bg-pink-400 hover:bg-pink-500 w-full '\
                 'text-white font-bold py-2 px-4 rounded-lg justify-center'
input_classes = 'border-2 rounded-lg w-full py-2 px-3 text-gray-700 '\
                'leading-tight appearance-none focus:outline-none '\
                'focus:border-pink-400'
label_classes = 'block uppercase tracking-wide text-gray-700 text-sm '\
                'font-semibold mx-3'
cart = model.Cart()
admin_sessions = {}

def display_pdp(product: model.Product, div: jp.Div) -> None:
    """Adds Product Detail Page of a product.
    
    Parameters:
    product (Product): product whose details will be displayed.
    div (Div): div the Product Detail Page will be rendered in.
    """
    def return_to_prev(caller, msg) -> None:
        """Returns to the page where display_pdp was called.
        
        Parameters:
        caller: Justpy object that triggers the event function.
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        # Deletes components in PDP and severs their connections
        for component in pdp_div.components:
            pdp_div.remove(component)
            component.delete()
        pdp_div.delete_components()
        # Deletes PDP container and severs its connections
        div.remove(pdp_div)
        pdp_div.delete()
        # Makes components in div show again
        for component in div.components:
            component.show = True

    def add_to_cart_click(caller, msg) -> None:
        """Adds item to cart if input and selections are valid and indicates
        errors or success in carrying out the operation.
        
        Parameters:
        caller: Justpy object that triggers the event function.
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        quantity = input_quantity.value
        color = color_select.value
        size = size_select.value
        indication = '' # Contains all indications to show the user
        # Adds indications alluding to inputs that are missing
        if quantity == '':
            indication += 'Debe indicar una cantidad. '
        if color == '':
            indication += 'Debe indicar un color. '
        if size == '':
            indication += 'Debe indicar una talla. '
        if indication == '':
            try:
                # Attempts adding item to cart and obtains string indicating
                # success of this attempt
                cart.add_item(product.product_id, quantity, color, size)
                indication = 'El producto se ha añadido al carrito.'
            except:
                indication = 'No hay suficientes unidades disponibles.'
        caller.indication_div.text = indication

    # Makes components in div stop showing
    for component in div.components:
        component.show = False
    # Adds container for PDP to div
    pdp_div = jp.Div(classes='flex flex-wrap relative justify-center my-5',
                     style='width:100%; height:100%; background-color:#fff;',
                     a=div)
    # Adds images
    image_div = jp.Div(a=pdp_div, style='width: 550px; height: 500px;',
                       classes='bg-gray-200 overflow-auto m-5 justify-center')
    for image in product.images.split('-'):
        image_div.add(jp.Img(src=f'/static/media/{image}',
                             classes='overflow-y-auto'))
    # Adds container for elements other than images
    text_div = jp.Div(a=pdp_div, classes='flex flex-col m-4 items-center '\
                      'lg:items-start w-3/4 lg:w-1/4')
    # Adds div that allows returning to previous page and closing PDP
    return_div = jp.Div(a=text_div, click=return_to_prev, classes='flex '\
                        'flex-wrap mb-2 cursor-pointer')
    return_icon = jp.Svg(xmlns='http://www.w3.org/2000/svg', 
                         classes='h-6 w-5', fill='none',
                         viewBox='0 0 24 24', stroke='black',
                         stroke_width='2', a=return_div)
    jp.Path(a=return_icon, stroke_linecap='round', stroke_linejoin='round',
            d='M15 19l-7-7 7-7')
    jp.P(a=return_div, text='Volver atrás')
    # Adds title, price and description
    md = jp.Div(a=text_div, classes='text-sm flex flex-row space-x-5')
    md.add(jp.P(text=f'ID: {product.product_id}'),
           jp.P(text=f'Disponibles: {product.available_units} unidades'))
    jp.P(a=text_div, text=product.name.title(), 
         classes='font-semibold text-2xl text-center '\
         'md:text-left break-words')
    jp.P(a=text_div, text=f'${product.price}',
         classes='text-2xl mb-2')
    if product.description != '.':
        jp.P(a=text_div, text=product.description.capitalize(),
             classes='text-sm mb-2')

    select_div = jp.Div(a=text_div, classes='grid grid-flow-row mb-2 '\
                        'w-full items-center')
    select_classes = 'rounded-md border-4 border-gray-200 mb-2 '\
                     'hover:bg-pink-400 text-sm'
    # Creates select object for sizes
    if product.sizes != '.':
        jp.P(a=select_div, text='Escoja una talla:', classes='text-sm')
        size_select = jp.Select(a=select_div, value='',
                                 classes=select_classes)
        for size in product.sizes.split('-'):
            size_select.add(jp.Option(value=size, text=size.capitalize()))
    else:
        size_select = jp.Select(value='No aplica')
    # Creates select object for colors
    if product.colors != '.':
        jp.P(a=select_div, text='Escoja un color:', classes='text-sm')
        color_select = jp.Select(a=select_div, value='',
                                 classes=select_classes)
        for color in product.colors.split('-'):
            color_select.add(jp.Option(value=color, text=color.capitalize()))
    else:
        color_select = jp.Select(value='No aplica')
    # Creates input object for quantity
    jp.P(a=select_div, text='Indique la cantidad:', classes='text-sm')
    input_quantity = jp.Input(a=select_div, type='number', value=1,
                              min=1, classes=f'{select_classes} '\
                              'text-center focus:border-pink-400')
    # Creates Add to Cart button
    add_to_cart_btn = jp.Button(a=text_div, text='AÑADIR AL CARRITO',
                                classes=button_classes)
    add_to_cart_btn.on('click', add_to_cart_click)
    cart_icon = jp.Svg(a=add_to_cart_btn, fill='white', 
                       viewBox='0 0 20 20', classes='h-5 w-5',
                       xmlns='http://www.w3.org/2000/svg')
    jp.Path(a=cart_icon, d='M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 '\
            '00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 '\
            '14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 '\
            '0017 3H6.28l-.31-1.243A1 1 0 005 1H3zM16 16.5a1.5 1.5 0 11-3 '\
            '0 1.5 1.5 0 013 0zM6.5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z')
    # Creates div showing indications about the Add to Cart operation
    add_to_cart_btn.indication_div = jp.Div(a=text_div, classes='text-sm '\
                                            'my-2 text-center text-pink-400')

def shop_section(section_div: jp.Div) -> None:
    """Adds components showcasing the available products, filtered by
    categories.
    
    Parameters:
    section_div (Div): Div the section will be rendered in.
    """
    def show_pdp(caller, msg) -> None:
        """Calls for the display of the Product Detail Page of a product on
        a Div.
        
        The product that will be displayed and the Div that the page will
        be rendered in are attributes of the caller.
        
        Parameters:
        caller: Justpy object that triggers the event function.
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        product = caller.product
        div = caller.d
        display_pdp(product, div)
        
    products_div = jp.Div(a=section_div, style='width: 100%; height: 100%;')
    jp.Br(a=products_div)
    # Adds navigation bar for categories
    category_nav_bar = model.TabsPills(a=products_div, classes='w-full',
                                       content_height='100%')
    for category in ['Todos los productos', 'Prendas Superiores',
                     'Pantalones', 'Faldas', 'Accesorios', 'Maquillaje']:
        products_div = jp.Div(classes='flex flex-wrap content-start '\
                              'place-content-around justify-center '\
                              'relative overflow-y-auto')
        # Gets available products
        result_proxy = db.get_table_objects(
            model.Product,
            model.Product.available_units > 0,
        )
        for row in result_proxy:
            if (category=='Todos los productos' 
                or (category!='Todos los productos' 
                    and row.category==category)):
                # Creates container for individual product layout
                product_layout = jp.Div(a=products_div, classes='flex '\
                                        'flex-col m-4 p-4 inline-block '\
                                        'items-center text-md font-semibold '\
                                        'hover:bg-gray-100 cursor-pointer '\
                                        'rounded-lg w-96')
                # Adds components to product layout
                image = row.images.split('-')[0]
                jp.Img(a=product_layout, src=f'/static/media/{image}',
                       classes='overflow-hidden w-full')
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
                    available_units=row.available_units,
                )
                product_layout.d = products_div
                product_layout.on('click', show_pdp)
        # Adds tab for category to category navigation bar
        category_nav_bar.add_tab(f'id{category}', f'{category}', products_div)

def about_section(section_div: jp.Div) -> None:
    """Adds components showing information about the shop and seller.
    
    Parameters:
    section_div (Div): Div the section will be rendered in.
    """
    content = file.get_file_content('perfil.txt')
    
    left_div = jp.Div(a=section_div, classes='md:w-1/2 flex flex-col m-10')
    jp.P(a=left_div, classes='text-pink-400 text-3xl font-semibold',
         text='Quiénes somos')
    jp.P(a=left_div, text=content['Quiénes somos'])
    
    right_div = jp.Div(a=section_div, classes='flex flex-col m-10')
    
    jp.P(a=right_div, classes='text-pink-400 text-2xl font-semibold pb-2',
         text='Contáctanos')
    d = jp.Div(a=right_div, classes='flex flex-row space-x-5')
    jp.Strong(a=d, text='Correo')
    jp.P(a=d, text=content['Correo'])

    jp.P(a=right_div, classes='text-pink-400 text-2xl font-semibold mt-5',
         text='Visítanos en redes')
    social_media_div = jp.Div(a=right_div, classes='flex flex-row space-x-5')
    for s in ['Instagram', 'TikTok']:
        link = jp.A(a=social_media_div, href=content[s])
        jp.Img(a=link, classes='w-12 h-12', src=f'/static/media/icon_{s}.png')
                
def display_order(order: model.Order, div: jp.Div,
                  in_admin_session: bool) -> None:
    """Adds components displaying the information of an order to a Div.
    
    Parameters:
    order (Order): Order that will be displayed.
    div (Div): Div the display will be rendered in.
    in_admin_session (bool): Indicates if function is called from Admin
    view.
    """
    def place_info(outer_div: jp.Div,
                   descriptions: dict[str, str|float]) -> None:
        """Places description/name to the left in bold and its corresponding
        content to its right within a Div.
        
        Parameters:
        outer_div (Dic): Div that components created within the function will
        be added to.
        descriptions (Dict): dict of information that will be displayed.
        """
        for desc in descriptions:
            d = jp.Div(a=outer_div, classes='flex flex-row space-x-4')
            jp.P(a=d, text=desc, classes='font-bold')
            jp.P(a=d, text=dic[desc])
    
    async def change_order_status(caller, msg) -> None:
        """Updates current order's status and reloads webpage to show changes.
        
        Parameters:
        caller: Justpy object that triggers the event function.
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        current_order = caller.current_order
        updated_status = model.OrderStatus(caller.value)
        current_order.update_status(updated_status)
        await admin_wp.reload()

    def return_to_prev(caller, msg) -> None:
        """Returns to the Consult Order page.
        
        Parameters:
        caller: Justpy object that triggers the event function.
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        # Deletes components in page showing order information and severs 
        # their connections
        for component in order_d.components:
            order_d.remove(component)
            component.delete()
        div.remove(order_d)
        order_d.delete()
        # Makes components in div show again
        for component in div.components:
            component.show = True
    
    # Makes components in div stop showing
    for component in div.components:
        component.show = False
    # Adds container for order
    order_d = jp.Div(a=div,
                     classes='space-y-3 flex flex-wrap w-full justify-center')
    dic = {
        'ID': order.order_id,
        'Creada': order.date,
        'Estado': order.status,
        'Nombre': order.buyer_name,
        'Teléfono': order.buyer_phone,
        'E-mail': order.buyer_email,
        'Localidad': f'{order.ship_city}, {order.ship_department}',
        'Dirección': order.ship_address,
        'Código postal': order.ship_zipcode,
        'Total': order.total,
    }
    # Adds container for header including order ID, date issued and status
    header = jp.Div(a=order_d, classes='flex flex-row justify-around w-full')
    if in_admin_session:
        # Places information and a select object for updating order status
        place_info(header, ['ID', 'Creada'])
        d = jp.Div(a=header, classes='flex flex-row space-x-4')
        jp.P(a=d, text='Estado', classes='font-bold')
        # Adds current order status as first option in select object
        order_status_select = jp.Select(a=d, value=dic['Estado'],
                                        classes='border-2 hover:bg-pink-400')
        order_status_select.current_order = order
        # Populates select object with other order status values
        for status in model.OrderStatus._value2member_map_:
            order_status_select.add(jp.Option(value=status, text=status))
        order_status_select.on('change', change_order_status)
    else:
        # Places information normally
        place_info(header, ['ID', 'Creada', 'Estado'])
    order_d.add(jp.Br())
    # Adds container for remaining details to the left of the container
    details_div = jp.Div(a=order_d,
                         classes='flex flex-col pb-8 lg:pb-0 '\
                         'justify-center overflow-auto lg:w-1/3')
    place_info(details_div, ['Nombre', 'Teléfono', 'E-mail'])
    details_div.add(jp.Br())
    place_info(details_div, ['Localidad', 'Dirección', 'Código postal'])
    details_div.add(jp.Br())
    place_info(details_div, ['Total'])
    # Gets order items from database
    order_items = db.get_table_objects(
        model.OrderItem,
        model.OrderItem.order_id == order.order_id,
    )
    # Adds container for order items table
    table_div = jp.Div(a=order_d, style='height: 240px',
                       classes='justify-center overflow-auto')
    if order_items != None:
        # Adds table for order items
        table = jp.AutoTable(
            a=table_div,
            values=[['ID', 'Nombre', 'Cantidad', 'Color', 'Talla']],
            classes='rounded-lg bg-gray-100 border-gray-200 table-auto '\
            'relative overflow-auto',
        )
        # Adds table content
        for item in order_items:
            # Verifies whether product related to item is in database
            if (product:=item.related_product) != None:
                table.values.append([item.product_id, product.name, 
                                     str(item.quantity), 
                                     item.color.capitalize(), 
                                     item.size.capitalize()])
            else:
                table.values.append([item.product_id,
                                     'Producto no disponible.',
                                     '-', '-', '-'])
    else:
        jp.Span(a=table_div, classes='text-center ', style='width: 300px',
             text='Ha ocurrido un error accediendo a los datos de la orden. '\
                  'Intenta más tarde. Si el problema persiste, envía un '\
                  'mensaje a nuestros medios de contacto.')
        
    if not in_admin_session:
        jp.Button(a=order_d, click=return_to_prev, text='Volver atrás',
                  classes=button_classes, style='width: 80%')
        
def consult_order_section(section_div: jp.Div) -> None:
    """Adds components that correspond to the Consult Order Section.
    
    The Consult Order Section primarily displays an input object that is
    meant to be filled with an order ID. Upon clicking on the button
    underneath it, the function will call for the display of the order's
    information if it exists and inform of the errors if it does not.
    
    Parameters:
    section_div (Div): Div the section will be rendered in.
    """
    def show_order(caller, msg) -> None:
        """Calls for the display of the input's corresponding order or
        informs the input is invalid.
        
        Parameters:
        caller: Justpy object that triggers the event function.
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        fetched_order = db.get_from_db(model.Order, caller.input_obj.value)
        caller.input_obj.value = ''
        if fetched_order == None:
            # Indicates no order with input ID exists
            caller.input_obj.placeholder = 'ID inválido'
        else:
            # Displays order with input ID
            caller.input_obj.placeholder = 'ID de orden'
            display_order(fetched_order, order_div, False)
            
    order_div = jp.Div(a=section_div, classes='border-2 border-gray-200 '\
                       'space-y-3 p-5 my-15 rounded-lg flex flex-wrap '\
                       'w-5/6 justify-center')
    jp.P(a=order_div, classes='text-center w-full',
         text='Ingresa el ID de orden para ver su estado actual')
    input_id = jp.Input(classes='border-2 text-center rounded-lg mx-40',
                        a=order_div, placeholder='ID de orden',
                        style='width: 400px;')
    consult_btn = jp.Button(a=order_div, classes=f'{button_classes} mx-40', 
                            style='width: 400px', text='Consultar')
    consult_btn.input_obj = input_id
    consult_btn.on('click', show_order)

def instructions_section(section_div: jp.Div) -> None:
    """Adds components showing answers to typical customer inquiries.
    
    Parameters:
    section_div (Div): Div the section will be rendered in.
    """
    content = file.get_file_content('ayuda.txt')
    
    div = jp.Div(a=section_div, classes='flex flex-col m-10',
                 style='width: 90%')
    for key in content.keys():
        jp.Strong(a=div, text=key)
        jp.P(a=div, text=content[key], classes='mb-5')

def cart_section(section_div: jp.Div) -> None:
    """Adds components corresponding to the Cart Section.
    
    The Cart Section displays the current session's cart and allows for its
    modification. Upon clicking on a checkout button, it will display a form
    to be filled with the buyer's data. Finally, upon submitting the form, it
    will attempt to create an order with the data and indicate the success of
    this operation. 
    
    Parameters:
    section_div (Div): Div the section will be rendered in.
    """
        
    async def reload_cart(msg) -> None:
        """Reloads content in cart section to show changes in cart items.
        
        Returns function that sets Cart Section's tab content.
        
        Parameters:
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        msg.new_tab = 'idCarrito'
        return await main_nav_bar.run_event_function('change', msg)
    
    async def delete_item(caller, msg) -> None:
        """Deletes item from cart and reloads tab content.
        
        Parameters:
        caller: Justpy object that triggers the event function; it contains
        the item to be deleted as an attribute.
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        cart.remove_item(caller.current_item)
        await reload_cart(msg)
    
    async def change_quantity(caller, msg) -> None:
        """Changes quantity of corresponding item by one unit if valid and
        reloads cart.
        
        The quantity change is valid if it does not make cart total quantity
        surpass maximmum and does not make item quantity lesser than one.
        
        Parameters:
        caller: Justpy object that triggers the event function; it contains
        a dict with the item to modify and the amount to add to its quantity.
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        try:
            caller.changes['item'].change_quantity(caller.changes['amount'])
            await reload_cart(msg)
        except:
            pass

    def submit_order_form(caller: jp.Form, msg) -> None:
        # TODO: add more strict validation
        data_dict = {}
        for input in msg.form_data:
            if input.name == 'Nombre':
                data_dict['name'] = input.value
            elif input.name == 'Correo electrónico':
                data_dict['email'] = input.value
            elif input.name == 'Teléfono':
                data_dict['phone'] = input.value
            elif input.name == 'Ciudad':
                data_dict['city'] = input.value
            elif input.name == 'Departamento':
                data_dict['department'] = input.value
            elif input.name == 'Dirección':
                data_dict['address'] = input.value
            elif input.name == 'Código Postal':
                data_dict['zipcode'] = input.value
        # Gets ID for new order
        new_order_id = db.get_new_id(model.Order.order_id)

        # Attempts placing order
        try:
            cart.place_order(new_order_id, data_dict)
            # Deletes form component, its components, and its connections
            for component in caller:
                caller.remove_component(component)
                component.delete()
            all_items_div.remove(caller)
            caller.delete()
            # Informs the user of the operation's success and shows 
            # them their order ID
            jp.P(a=all_items_div, classes='text-center px-20 py-5',
                text='Su orden fue creada exitosamente con el ID '\
                f'{new_order_id}. Recuerde su ID para poder consultar '\
                'los detalles de su orden.')
        except:
            # Informs the user of the failure
            jp.P(a=all_items_div, classes='text-center px-20 py-5',
                 text='Su orden no puede crearse en este momento.')
            
    def checkout(caller: jp.Button, msg) -> None:
        """Displays form for user to input their information.
        
        Upon submitting the form, it checks if information is valid. If it 
        is, it places an order with the gathered information, otherwise, it
        notifies the user about the error.
        
        Parameters:
        caller: Justpy object that triggers the event function.
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        # Stops Checkout button
        caller.show = False
        # Adds form for buyer's information
        jp.Br(a=all_items_div)
        form = jp.Form(a=all_items_div, style='height: 290px',
                       classes='flex flex-wrap flex-col justify-start '\
                       'space-x-5')
        # TODO: add drop-down menu for Ciudad, Departamento
        for label_text in ['Nombre', 'Correo electrónico',
                           'Teléfono', 'Ciudad', 'Departamento',
                           'Dirección', 'Código Postal']:
            label = jp.Label(a=form, text=label_text, 
                             classes=label_classes)
            if label_text == 'Teléfono':
                label.for_component = jp.Input(name=label_text, 
                                               classes='form-input mb-2',
                                               type='tel', required=True,
                                               pattern='[0-9]{3}-[0-9]{3}-[0-9]{4}',
                                               placeholder='123-4567-8901',
                                               a=form)
            elif label_text == 'Correo electrónico':
                label.for_component = jp.Input(name=label_text, 
                                               classes='form-input mb-2',
                                               required=True, type='email',
                                               a=form)
            elif label_text == 'Código Postal':
                label.for_component = jp.Input(name=label_text, 
                                               classes='form-input mb-2', 
                                               maxlength=6, required=True,
                                               minlength=6, a=form)
            else:
                label.for_component = jp.Input(a=form, name=label_text, 
                                               classes='form-input mb-2',
                                               required=True)
        submit_button = jp.Input(value='Finalizar compra', type='submit',
                                 a=form, classes=f'{button_classes} mt-2')
        submit_button.remove_class('w-full')
        form.on('submit', submit_order_form)
    
    # Adds container for cart items
    all_items_div = jp.Div(a=section_div, classes='overflow-auto m-6', style='width: 980px')
    # Adds headers
    item_div = jp.Div(a=all_items_div, 
                      classes='grid grid-cols-12 text-center py-2 border-b-2')
    for header in ['ID', 'Nombre', 'Cantidad', 'Color', 'Talla', 'Total', '']:
        if header == 'Nombre':
            jp.P(a=item_div, text=header, classes='col-span-3')
        elif header in ('Color', 'Talla', 'Total'):
            jp.P(a=item_div, text=header, classes='col-span-2')
        else:
            jp.P(a=item_div, text=header)
    # Adds content
    if len(cart.cart_items) > 0:
        for item in cart.cart_items:
            item_div = jp.Div(a=all_items_div, classes='grid grid-cols-12 '\
                            'text-center py-2 border-b-1')
            if (product:=item.related_product) != None:
                # Adds item information if the product it is related to exists
                for attribute in (item.product_id, product.name, item.quantity,
                            item.color, item.size, item.item_total):
                    if attribute == product.name:
                        jp.P(a=item_div, text=attribute, 
                            classes='col-span-3')
                    elif attribute in (item.color, item.size, item.item_total):
                        jp.P(a=item_div, text=str(attribute).capitalize(), 
                            classes='col-span-2')
                    elif attribute == item.quantity:
                        quantity_div = jp.Div(classes='flex flex-row '\
                                            'justify-center items-center',
                                            a=item_div)
                        # Adds minus icon
                        minus_icon = jp.Svg(xmlns='http://www.w3.org/2000/svg',
                                        classes='h-4 w-4 cursor-pointer',
                                        fill='black', viewBox='0 0 20 20',
                                        a=quantity_div)
                        jp.Path(a=minus_icon, fill_rule='evenodd',
                                clip_rule='evenodd',
                                d='M3 10a1 1 0 011-1h12a1 1 0 110 '\
                                '2H4a1 1 0 01-1-1z')
                        minus_icon.changes = {'item': item, 'amount': -1}
                        minus_icon.on('click', change_quantity)
                        # Adds item quantity
                        jp.P(a=quantity_div, text=attribute, classes='px-2')
                        # Adds plus icon
                        plus_icon = jp.Svg(xmlns='http://www.w3.org/2000/svg',
                                        classes='h-4 w-4 cursor-pointer',
                                        fill='black', viewBox='0 0 20 20',
                                        a=quantity_div)
                        jp.Path(a=plus_icon, fill_rule='evenodd', 
                                clip_rule='evenodd',
                                d='M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 '\
                                '0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z')
                        plus_icon.changes = {'item': item, 'amount': 1}
                        plus_icon.on('click', change_quantity)
                    else:
                        jp.P(a=item_div, text=attribute)
            else:
                # Adds indication informing the user if the product is not 
                # currently available
                jp.P(a=item_div, text=item.product_id)
                jp.P(a=item_div, classes='col-span-11',
                    text='Este producto no se encuentra disponible.')
                
            # Adds X icon for the item's deletion
            x_icon = jp.Svg(xmlns='http://www.w3.org/2000/svg', 
                            classes='class="ml-4 h-6 w-6 cursor-pointer',
                            viewBox='0 0 20 20', fill='gray', a=item_div)
            jp.Path(a=x_icon, fill_rule='evenodd', clip_rule='evenodd',
                    d='M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 '\
                    '0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 '\
                    '1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 '\
                    '10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 '\
                    '7.293z')
            x_icon.current_item = item
            x_icon.on('click', delete_item)
    else:
        msg_div = jp.Div(a=all_items_div, classes='grid grid-cols-12 '\
                          'text-center py-2')
        jp.P(a=msg_div, classes='col-span-12 py-5', 
             text='No hay productos en el carrito aún.')

    # TODO: calculate delivery fee
    delivery_fee = 0
    # Adds container for cart summary
    summary_div = jp.Div(a=section_div, style='width: 280px',
                         classes='flex flex-col bg-gray-200 p-5 mx-5 my-6 '\
                         'rounded-lg')
    jp.P(a=summary_div, text='RESUMEN DE COMPRA',
         classes='font-semibold text-center text-lg mb-2')
    total_div = jp.Div(a=summary_div, classes='grid grid-cols-2')
    total_div.add(
        jp.P(text='Subtotal', classes='font-semibold text-left'),
        jp.P(text=cart.cart_total, classes='text-right'),
        jp.P(text='Envío', classes='font-semibold text-left'),
        jp.P(text=delivery_fee, classes='text-right'),
        jp.P(text='Total', classes='font-semibold text-left mt-1'),
        jp.P(text=(cart.cart_total+delivery_fee), classes='text-right mt-1'),
    )
    # Adds Checkout button
    if cart.cart_total+delivery_fee > 0:
        checkout_btn = jp.Button(a=summary_div, text='Finalizar compra',
                                 classes=f'{button_classes} mt-2')
        checkout_btn.on('click', checkout)

def admin_section_login(section_div: jp.Div) -> None:
    """Adds components showing Admin login form and leads to Admin page if
    form is valid.
    
    Parameters:
    section_div (Div): Div the section will be rendered in.
    """
    def validate_user(form: jp.Form, msg) -> None:
        """Validates login form. Redirects to Admin page if valid and
        informs of error if not.
        
        Parameters:
        form (Form): Admin form to be validated.
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        # TODO: re-implement user validation through a method ?
        psw_hasher = model.PasswordHasher()
        correct_user = file.get_content_by_field('admin.txt', 'Usuario')
        user_is_valid = True
        for input in msg.form_data:
            # Verifies input username and password are correct
            if ((input.name=='usuario' and input.value!=correct_user)
                or (input.name=='clave' and not psw_hasher.verify_password(input.value))):
                user_is_valid = False
                break
        if user_is_valid:
            # Allows access to admin section from the current session and 
            # redirects page to admin section
            admin_sessions[msg.session_id] = True
            msg.page.redirect = '/admin'
        else:
            # Shows user text indicating error
            form.error_indication.text = 'Contraseña o usuario incorrectos.'
    
    form_div = jp.Div(classes='m-10 w-1/4', a=section_div)
    # Adds login form
    login_form = jp.Form(a=form_div, classes='px-4 py-7')
    username_label = jp.Label(a=login_form, text='Usuario', 
                              classes=label_classes)
    username_label.for_component = jp.Input(a=login_form, name='usuario',
                                            placeholder='Usuario',
                                            classes=input_classes
                                            + ' mb-3 form-input')
    password_label = jp.Label(a=login_form, text='Contraseña', 
                              classes=label_classes)
    password_label.for_component = jp.Input(a=login_form, name='clave',
                                            type='password',
                                            placeholder='************',
                                            classes=input_classes
                                            + ' mb-3 form-input')
    jp.Button(a=login_form, text='Iniciar sesión', 
              classes=button_classes+' mb-2', type='submit')
    # Adds div where indication of error will be displayed if necessary
    login_form.error_indication = jp.Div(a=login_form,
                                         classes='text-red-500 text-sm text-center')
    login_form.on('submit', validate_user)

main_sections = [
    model.Section('Productos', shop_section),
    model.Section('Acerca de Buhi', about_section),
    model.Section('Consultar Orden', consult_order_section),
    model.Section('Ayuda', instructions_section),
    model.Section('Carrito', cart_section),
    model.Section('Admin', admin_section_login),
]

@jp.SetRoute('/main')  
def main_page() -> jp.WebPage:
    """Returns main webpage with all of its components."""

    def reload_content(caller, msg) -> None:
        """Reloads content on the tab that is clicked on.
        
        Parameters:
        caller (TabPills): object that triggers the event function.
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        for section in main_sections:
            if f'id{section.name}' == msg.new_tab:
                section_div = jp.Div(style=caller.wrapper_style)
                section.link(section_div)
                for tab in caller.tabs:
                    if tab['id'] == msg.new_tab:
                        tab['content'] = section_div
                        caller.set_content_div(tab)
                        break
    
    global main_nav_bar
    main_wp = jp.WebPage(template_file='tailwindui.html')
    # Sets the font that will be used
    main_wp.head_html = '<link rel="preconnect" href="https://fonts.googleapis.com">'\
                        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'\
                        '<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,600;0,700;1,700&display=swap" rel="stylesheet">'
    main_wp.css = 'body { font-family: \'Poppins\', sans-serif; }'
    # Creates main container
    wp_div = jp.Div(classes='flex flex-col', a=main_wp,
                    style='font-family: \'Poppins\'')
    # Adds header
    title_header = jp.Div(a=wp_div,
                          classes='w-full flex flex-shrink bg-pink-400 '\
                          'text-white text-6xl font-bold justify-center '\
                          'items-center')
    title_header.add(jp.Img(src='/static/media/logo.png',
                            classes='h-12 mx-3'))
    title_header.add(jp.Strong(text='Buhi Store', classes='my-2'))
    # Adds navigation bar and tabs
    main_nav_bar = model.TabsPills(a=wp_div, classes='w-full', 
                                   content_height='100%',
                                   tab_list_bg='black', 
                                   hover_bg='gray-900',
                                   text_color='white')
    for section in main_sections:
        section_div = jp.Div(style=model.TabsPills.wrapper_style)
        # Adds section content to container
        section.link(section_div)
        # Adds tab with section content
        main_nav_bar.add_tab(f'id{section.name}', f'{section.name.upper()}', 
                             section_div)
        main_nav_bar.on('change', reload_content)
        
    return main_wp


def display_all_orders(section_div: jp.Div) -> None:
    """Adds components displaying all orders and their respective information.
    
    Parameters:
    section_div (Div): Div the section will be rendered in.   
    """
    # Gets all orders from database
    all_orders = db.get_table_objects(model.Order)
    jp.Br(a=section_div)
    # Displays orders if there are any
    if len(all_orders) > 0:
        for order in all_orders:
            order_div = jp.Div(a=section_div,
                               classes='border-2 border-gray-200 space-y-3 '\
                               'p-5 my-15 rounded-lg flex flex-wrap w-5/6 '\
                               'justify-center')
            display_order(order, order_div, True)
    else:
        jp.P(a=section_div, text='No hay órdenes que mostrar.',
             classes='text-center text-lg m-10')
    
def modify_products(section_div: jp.Div) -> None:
    pass

def add_products(section_div: jp.Div) -> None:
    pass

def modify_profile(section_div: jp.Div) -> None:
    pass

admin_sections = [
    model.Section('Órdenes', display_all_orders),
    model.Section('Modificar Productos', modify_products),
    model.Section('Añadir Productos', add_products),
    model.Section('Modificar Perfil', modify_profile),
]

def valid_session(f):
    # TODO: check if valid_session has to be reimplemented as a method
    @wraps(f)
    def wrapper(request) -> (Any | jp.WebPage):
        # Allows access to admin section if admin is logged in in the current
        # session ID, otherwise, it redirects the user to main webpage
        if request.session_id in admin_sessions:
            return f(request)
        else:
            return jp.redirect('/main')
    return wrapper

@jp.SetRoute('/admin')
@valid_session
def admin_section(request) -> jp.WebPage:
    """Returns admin webpage with all of its components."""
    global admin_wp
    
    def return_to_main(caller, msg) -> None:
        """Redirects to main webpage."""
        msg.page.redirect = '/main'
        
    def reload_content(caller, msg) -> None:
        """Reloads content on the tab that is clicked on.
        
        Parameters:
        caller (TabPills): object that triggers the event function.
        msg: Contains information about the event (is sent automatically as
        parameter alongside caller).
        """
        for section in admin_sections:
            if f'id{section.name}' == msg.new_tab:
                section_div = jp.Div(style=caller.wrapper_style)
                section.link(section_div)
                for tab in caller.tabs:
                    if tab['id'] == msg.new_tab:
                        tab['content'] = section_div
                        caller.set_content_div(tab)
                        break
    
    admin_wp = jp.WebPage(template_file='tailwindui.html')
    # Sets the font that will be used
    admin_wp.head_html = '<link rel="preconnect" href="https://fonts.googleapis.com">'\
                         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'\
                         '<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,600;0,700;1,700&display=swap" rel="stylesheet">'
    admin_wp.css = "body { font-family: 'Poppins', sans-serif; }"
    wp_div = jp.Div(classes='flex flex-col', a=admin_wp, style='font-family: \'Poppins\'')  # Creates main container
    # Adds div that will allow returning to main webpage
    return_div = jp.Div(a=wp_div,
                        classes='w-full flex flex-shrink bg-pink-400 '\
                        'text-white text-2xl font-bold justify-center '\
                        'items-center hover:bg-pink-500')
    return_div.add(jp.Strong(text='Volver a página principal', classes='my-2'))
    return_div.on('click', return_to_main)
    # Adds navigation bar and tabs
    admin_nav_bar = model.TabsPills(a=wp_div, classes='w-full', 
                                    content_height='100%',
                                    tab_list_bg='black', 
                                    hover_bg='gray-900',
                                    text_color='white')
    for section in admin_sections:
        section_div = jp.Div(style=model.TabsPills.wrapper_style)
        # Adds section content to container
        section.link(section_div)
        # Adds tab with section content
        admin_nav_bar.add_tab(f'id{section.name}', f'{section.name.upper()}', 
                              section_div)
        admin_nav_bar.on('change', reload_content)
        
    return admin_wp

jp.justpy(main_page)
