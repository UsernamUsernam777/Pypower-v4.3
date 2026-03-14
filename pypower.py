import _datetime
import ast as _ast
import customtkinter as _ctk
import pyperclip as _pyperclip
import time as _time
import webbrowser as _webbrowser
import os as _os
import subprocess as _subprocess
import random as _random
class Time:
    @staticmethod
    def random_time(method=12, with_sec=True):
        if method == 12:
            hours = list(range(1, 13))
        else:
            hours = list(range(24))
        result = f"{_random.choice(hours):02}:{_random.randint(0, 59):02}"
        if with_sec:
            result += f':{_random.randint(0, 59):02}'
        return result
    def minus_clock(time_str1, time_str2):
        t1 = Time.reverse_many_hms(time_str1)
        t2 = Time.reverse_many_hms(time_str2)
        return Time.how_many_hms_in_s(abs(t1-t2))
    """convert time to type_output"""
    def convert_to_iterable_and_int(time_str, type_output=tuple):
        """Convert 'HH:MM:SS' string to an iterable of ints. ex: '01:30:45' -> (1, 30, 45)"""
        return type_output(map(int, time_str.split(':')))
    def how_many_hms_in_s(sec):
        """how many hours, minutes and seconds in seconds"""
        hours = sec // 3600
        minutes = (sec % 3600) // 60
        seconds = (sec % 3600) % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    def reverse_many_hms(time_str):
        result = Time.convert_to_iterable_and_int(time_str)
        return (result[0]*3600) + (result[1]*60) + result[2]
class Other:
    @staticmethod
    def copy_pypower(path):
        """Copy the contents of pypower.py to the clipboard."""
        with open(path, 'r', encoding='utf-8') as f:
            _pyperclip.copy(f.read())
    def search_google(text):
        """Open a new browser tab with a Google search for text."""
        _webbrowser.open_new_tab(f"https://www.google.com/search?q={text}&oq=&gs_lcrp=EgZjaHJvbWUqCQgAECMYJxjqAjIJCAAQIxgnGOoCMgkIARAjGCcY6gIyCQgCEEUYOxjCAzIRCAMQABgDGEIYjwEYtAIY6gIyDwgEEC4YAxiPARi0AhjqAjIRCAUQABgDGEIYjwEYtAIY6gIyEQgGEAAYAxhCGI8BGLQCGOoCMg8IBxAuGAMYjwEYtAIY6gLSAQg0MDVqMGoxNagCCLACAfEF1j7Fc7lEloM&sourceid=chrome&ie=UTF-8")
    def in_bg(name, duration, action=None):
        """Run action in a background thread after duration seconds.
don't write repeated name."""
        import threading as _threading
        names = [i.name for i in _threading.enumerate()]
        if name not in names:
            def v():
                _time.sleep(duration)
                if action:
                    action()
            a = _threading.Thread(name=name, target=v, daemon=True)
            a.start()
class Apps:
    @staticmethod
    def create_app(path, icon=None, move_to_folder=None):
        """Build a standalone .exe from a .py file using PyInstaller, then clean up build files."""
        def mainloop():
            if not _os.path.exists(path):
                print('Error!')
            else:
                pj = _os.path.dirname(path)
                n_py = _os.path.basename(path)
                n_exe = _os.path.basename(path).replace('.py', '.exe')
                n_spec = _os.path.basename(path).replace('.py', '.spec')
                pro = ['pyinstaller', '--onefile', '--windowed', n_py]
                _os.chdir(pj)
                if icon:
                    pro.append(f'--icon={icon}')
                p = _subprocess.Popen(pro, creationflags=_subprocess.CREATE_NO_WINDOW)
                p.wait()
                if _os.path.exists(_os.path.join('dist', n_exe)):
                    _os.replace(_os.path.join('dist', n_exe), _os.path.join(pj, n_exe))
                if _os.path.exists(_os.path.join(pj, n_exe)):
                    _os.system('rmdir /s /q dist')
                    _os.system('rmdir /s /q build')
                    _os.remove(n_spec)
                if _os.path.exists(path.replace('.py', '.exe')):
                    if move_to_folder:
                        new = _os.path.join(move_to_folder, n_exe)
                        _os.replace(path.replace('.py', '.exe'), new)
                    else:
                        new = path.replace('.py', '.exe')
                    print(f"App Created Successed in {new}")
        Other.in_bg('create app loading ...', 1, mainloop)
class Files:
    @staticmethod
    def read_write_txt_file(file_txt, do='read', text=None):
        if do == 'read':
            with open(file_txt, 'r', encoding='utf-8') as f:
                return f.read().strip()
        else:
            with open(file_txt, 'w', encoding='utf-8') as f:
                f.write(text or '')
    def make_if_not_exists(path, type=''):
        """Create a folder (type='') or empty file at path if it doesn't exist."""
        if not _os.path.exists(path):
            if type == '':
                _os.mkdir(path)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    pass
    def append_to_pypower(path, class_name, code):
        """Append a labeled code block to pypower.py."""
        Files.append_to_file(path, f'\n#{class_name}\n'+code)
    def append_to_file(path, text, side='bottom'):
        """Append text to a file removing double blank lines."""
        with open(path, 'r', encoding='utf-8') as a:
            old_text = a.read()
        with open(path, 'w', encoding='utf-8') as b:
            if side == 'top':
                new_text = text + '\n' + old_text
            else:
                new_text = old_text + '\n' + text
            b.write(new_text.replace('\n\n', '\n'))
class GUI:
    @staticmethod
    class CustomTk:
        def add_texts_to_file(master, file, sep='\n'):
            Files.make_if_not_exists(file, 'txt')
            Files.read_write_txt_file(file, 'write', '')
            for i in GUI.CustomTk.has_text(GUI.CustomTk.all_objects(master), return_dic_widget_texts=True)['texts']:
                Files.append_to_file(file, i+sep)
        def has_text(iterable, with_empty=False, return_dic_widget_texts=False):
            result = []
            for i in iterable:
                try:
                    if not with_empty:
                        if i.cget('text').strip():
                            result.append(i)
                    else:
                        result.append(i)
                except:
                    pass
            if return_dic_widget_texts:
                return {'texts': [i.cget('text') for i in result], 'widgets': result}
            return result
        def double_clk_copy_label(label):
            def co(e):
                _pyperclip.copy(label.cget('text'))
                def place():
                    x = label.winfo_x() - label.winfo_width() // 2
                    y = label.winfo_y() + label.winfo_height()
                    GUI.CustomTk.show_hide_message(label.master, 'Copied!', text_color='green', x=x, y=y)
                label.after(200, place)
            label.bind('<Double-Button-1>', co)
        def show_hide_message(master, message, text_color='red', font=('arial', 30), x=None, y=None, hide_after=1, in_btn=False):    
            if in_btn:
                a = _ctk.CTkButton(master, text=message, font=font, text_color=text_color, hover=False, )
            else:
                a = _ctk.CTkLabel(master, text=message, font=font, text_color=text_color)
            if x and y:
                a.place(x=x, y=y)
            else:
                a.pack()
            a.after(hide_after*1000, a.destroy)
            return a
        def change_mode(master, light_icon='light', dark_icon='dark'):
            def c():
                if _ctk.get_appearance_mode() == 'Dark':
                    _ctk.set_appearance_mode('Light')
                    button.configure(text=dark_icon)
                else:
                    _ctk.set_appearance_mode('Dark')
                    button.configure(text=light_icon)
            button = _ctk.CTkButton(master, text=dark_icon, command=c, font=('arial', 30))
            return button
        def in_point(widgets, x, y):
            return [w for w in widgets if w.winfo_x() == x and w.winfo_y() == y]
        def limit_len(entry, limit):
            if entry.cget('textvariable'):
                check = entry.cget('textvariable')
            else:
                check = _ctk.StringVar()
            def c(*args):
                if len(entry.get()) > limit:
                    entry.delete(len(entry.get())-1)
            entry.configure(textvariable=check)
            check.trace_add('write', c)
        def disable_button(button):
            button.configure(fg_color='#e1e3e1', text_color='white', command=None, hover=False)
        def sync_entry_with_label(entry, label):
            if entry.cget('textvariable'):
                var = entry.cget('textvariable')
            else:
                var = _ctk.StringVar()
            var.trace_add('write', lambda *args:label.configure(text=entry.get()))
            entry.configure(textvariable=var)
        def console(master, texts, per_row=3, entry_to_insert=None, font=('arial', 20), text_color='white', return_dic_frame_and_buttons=False):
            result = _ctk.CTkFrame(master)
            def create_button(text):
                if entry_to_insert:
                    return _ctk.CTkButton(result, text=text, font=font, text_color=text_color, command=lambda: entry_to_insert.insert('end', text))
                return _ctk.CTkButton(result, text=text, font=font, text_color=text_color)
            buttons = [create_button(str(c)) for c in texts]
            GUI.CustomTk.tidy_up(buttons, per_row=per_row)
            if return_dic_frame_and_buttons:
                return {'frame': result, 'buttons': buttons}
            return result
        def console_num(master, per_row=3, entry_to_insert=None, font=('arial', 20), text_color='white'):
            return GUI.CustomTk.console(master, range(10), per_row, entry_to_insert, font=font, text_color=text_color)
        class Timer:
            def __init__(self, duration, obj, start_icon='start', stop_icon='stop', when_finish=None):
                self.duration = duration
                self.resume = self.duration > 0
                self.obj = obj
                self.button = _ctk.CTkButton(obj.master, text=start_icon, command=self.start)
                self.start_icon = start_icon
                self.stop_icon = stop_icon
                self.timers = 0
                self.when_finish = when_finish
            def start(self):
                self.button.configure(command=self.stop, text=self.stop_icon)
                def m():
                    while self.resume:
                        self.duration -= 1
                        self.obj.configure(text=Time.how_many_hms_in_s(self.duration))
                        _time.sleep(1)
                        if self.when_finish and self.duration == 0:
                            self.button.configure(text=self.start_icon)
                            self.when_finish()
                            break
                Other.in_bg(f'{id(self.obj)}', 0, m)
            def stop(self):
                self.button.configure(command=self.resume_timer, text=self.start_icon)
                self.resume = False
            def resume_timer(self):
                self.resume = self.duration > 0
                self.start()
        def show_hide_entry_btn(entry, show_ico="show", hide_ico='hide', hide_with="*"):
            entry.configure(show=hide_with)
            btn = _ctk.CTkButton(entry.master, text=show_ico, font=("arial", 20))
            def change():
                if entry.cget("show") == hide_with:
                    entry.configure(show='')
                    btn.configure(text=hide_ico)
                else:
                    entry.configure(show=hide_with)
                    btn.configure(text=show_ico)
            btn.configure(command=change)
            return btn
        def move(obj):
            master = obj.master
            def m(e):
                x = obj.winfo_x()
                y = obj.winfo_y()
                obj.pack_forget()
                obj.grid_forget()
                obj.place(x=x, y=y)
                width = obj.winfo_width()
                height = obj.winfo_height()
                mouse_x = master.winfo_pointerx() - master.winfo_rootx() - width//2
                mouse_y = master.winfo_pointery() - master.winfo_rooty() - height//2
                obj.place(x=mouse_x, y=mouse_y)
            obj.bind('<B1-Motion>', m)
        def good_size(widgets):
            """resize widgets with the biggest size (height, width)"""
            def m():
                width = [i.winfo_reqwidth() for i in widgets]
                height = [i.winfo_reqheight() for i in widgets]
                for i in widgets:
                    i.configure(width=max(width), height=max(height))
            Other.in_bg('good size', 0, m)
        def tidy_up(widgets, per_row, start_row=0, start_column=0, padx=5, pady=5):
            master = widgets[0].master
            def m():
                nonlocal start_row
                """
                Arrange widgets in a grid with a fixed number per row.
                """
                for i in range(start_row+1):
                    master.grid_rowconfigure(i, minsize=widgets[0].winfo_reqheight())
                for i in range(start_column+1):
                    master.grid_columnconfigure(i, minsize=widgets[0].winfo_reqwidth())
                columns = start_column
                allowed_num = 0
                multy = Math.number_multiplies(per_row, len(widgets), set)
                for w in widgets:
                    w.grid(column=columns, row=start_row, padx=padx, pady=pady)
                    allowed_num += 1
                    columns += 1
                    if allowed_num in multy:
                        start_row += 1
                        columns = start_column
            master.after(len(widgets) // 1000, m)
        def all_objects(master):
            """Return a flat list of all child widgets in master."""
            result = []
            for i in master.winfo_children():
                if isinstance(i, (_ctk.CTkFrame, _ctk.CTkScrollableFrame)):
                    result.extend(GUI.CustomTk.all_objects(i))
                else:
                    result.append(i)
            return result
        def edit_all_widgets_texts(iterable, font='arial', size=20, text_color='lightblue', bg='', with_empty=False):
            """Apply font, text color, and background to all child widgets in master."""
            def m():
                for i in GUI.CustomTk.has_text(iterable, with_empty=with_empty):
                    if bg:
                        i.configure(font=(font, size), text_color=text_color, fg_color=bg)    
                    else:
                        i.configure(font=(font, size), text_color=text_color, fg_color='transparent')
            Other.in_bg('edit_all_texts', 0.5, m)
        def info(widget, information, font='arial', size=20, bg='', hide_after=5):
            """Show a tooltip label below widget on hover, auto-hide after hide_after seconds."""
            if bg:
                inf = _ctk.CTkLabel(widget.master, text=information, font=(font, size), fg_color=bg)
            else:
                inf = _ctk.CTkLabel(widget.master, text=information, font=(font, size), fg_color='transparent')
            inf.lift()
            def show(e):
                x = widget.winfo_x()
                y = widget.winfo_y()
                inf.after(500, lambda: inf.place(x=x, y=y+widget.winfo_height()))
                inf.after(hide_after*1000, inf.place_forget)
            widget.bind('<Enter>', show)
        def mouse_wheel_num(entry, end, step=1):
            """Scroll through numbers inside an entry with the mouse wheel."""
            def f(e):
                if Math.int_or_float(entry.get()):
                    a = float(entry.get())
                    entry.delete(0, 'end')
                    if e.delta >= 1:
                        new_num = type(step)(a + step)
                    else:
                        new_num = type(step)(a - step)
                    if a == end:
                        new_num = 0
                    entry.insert(0, round(new_num, 2))
            entry.bind("<MouseWheel>", f)
    class Turtle:
        def in_circle(turtle_obj, shape_as_func, how_many=10):
            """draw shape_as_func in circle"""
            for i in range(how_many):
                shape_as_func()
                turtle_obj.left(360/how_many)
        def rock_bottom(window, obj, before_end=0):
            x = window.window_width() // 2 - before_end
            y = window.window_height() // 2 - before_end
            return abs(obj.xcor()) >= abs(x) or abs(obj.ycor()) >= abs(y)
        def move(obj, distance, direction='forward'):
            """Move a Turtle object without drawing (pen up then down)."""
            if direction in ['backward', 'forward']:
                obj.penup()
                if direction == 'forward':
                    obj.fd(distance)
                elif direction == 'backward':
                    obj.bk(distance)
                obj.pendown()
            else:
                print('Invalid direction!')
class String:
    def __init__(self, text):
        self.text = text
    def super_join(self, sep, after_how_many_letters):
        """Insert sep every after_how_many_letters characters in the string."""
        value = 0
        new = ''
        ran = Math.number_multiplies(after_how_many_letters, len(self.text)-1)
        for i in self.text:
            new += i
            value += 1
            if value in ran:
                new += sep
        return new
    def reverse(self, sep):
        """Reverse the order of parts split by sep. ex: 'a-b-c' -> 'c-b-a'"""
        return f'{sep}'.join(self.text.split(sep)[::-1])
    def replace_objects_with_one(self, iterable, new_obj=''):
        """Replace every character found in iterable with new_obj."""
        result = ''
        for i in self.text:
            if i not in iterable:
                result += i
            else:
                result += new_obj
        return result
    def replace_many(self, old_iterable, new_iterable):
        """Replace each character in old_iterable with the matching one in new_iterable."""
        result = ''
        for i in self.text:
            if i in old_iterable:
                result += new_iterable[old_iterable.index(i)]
            else:
                result += i
        return result
    def between(self, c1, c2):
        """return string between two points"""
        result = []
        index = [Iterable.indexes(self.text, c1), Iterable.indexes(self.text, c2)]
        for i, e in zip(index[0], index[1]):
            result.append(self.text[i:e+1])
        return result
class Iterable:
    @staticmethod
    def search_iterable(iterable, search_with, ignore_case=True):
        result = []
        for o in iterable:
            if ignore_case:
                if str(search_with).lower() in str(o).lower():
                    result.append(o)
            else:
                if str(search_with) in str(o):
                    result.append(o)
        return result
    def numred(iterable):
        """numred the objects in an iterable ex: if you want to create numred tasks
            numred(['visiting my uncle', 'water the plants'])  1.visiting my uncle"""
        result = ''
        for i in range(len(iterable)):
            result += f"{i+1}. {iterable[i]}\n"
        return result.strip()
    def indexes(iterable, obj):
        return [i for i in range(len(iterable)) if iterable[i] == obj]
    def replace_iterable(iterable, index, new_obj=None):
        """replace an object by it's index with new_obj ex:    replace(['mike', 'mark'], 1, 'Olivia')
result = ['Olivia', 'mark']"""
        co = iterable.copy()
        if new_obj:
            co[index-1] = new_obj
        else:
            co.remove(co[index-1])
        return co
    def all_in(main_iterable, iterable):
        """Checks if all unique elements of 'iterable' exist within 'main_iterable'."""
        return set(iterable).issubset(set(main_iterable))
    class Dict:
        def swap_dict(dic):
            """k: v ➡ v, k"""
            result = {}
            for k, v in dic.items():
                if isinstance(v, (list, tuple, set, dict)):
                    v = str(v)
                result[v] = k
            return result
        def return_dict_in_lines(dec):
        """Return a dict formatted as 'key: value' lines."""
            result = ''
            for i in dec:
                result += f"{i}: {dec[i]}\n"
            return result.strip()
class Math:
    @staticmethod
    def int_or_float(num):
        try:
            num = str(num).strip()
            float(num)
            assert num[-1] != '.'
            return True
        except:
            return False
    def iter_num(iterable):
        """Return sum, average, max, and min of an iterable as a dict."""
        return {'sum': sum(iterable), 'average': sum(iterable) / len(iterable), 'max': max(iterable), 'min': min(iterable)}
    def number_multiplies(num, end, type=list):
        """Return all multiples of num up to end. ex: number_multiplies(3, 9) -> [3, 6, 9]"""
        return type(range(num, end+1, num))
    def arrays(array, step, show='lists'):
        """Split a range into consecutive [start, end] pairs by step.
        If show != 'lists', return a formatted string instead."""
        result = []
        for i in range(step, array, step):
            result.append([i, i+step])
        if show != 'lists':
            result2 = ''
            for i, e in result:
                result2 += str((i, e)).replace('(', '').replace(')', '').replace(', ', ' - ')+'\n'
            return result2.strip()
        return result
