from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from ..database import Database

class ScheduleScreen(Screen):
    def __init__(self, **kwargs):
        super(ScheduleScreen, self).__init__(**kwargs)
        self.name = 'schedule'
        self.db = Database()
        self.selected_date = ''
        self.selected_image = None
        self.build_schedule()

    def build_schedule(self):
        self.clear_widgets()

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 헤더 (날짜 표시 및 뒤로 가기)
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')

        back_button = Button(text='< back', size_hint_x=None, width='100dp')
        back_button.bind(on_press=self.go_back)

        self.date_label = Label(text='날짜를 선택해 주세요', font_size='18sp')

        header_layout.add_widget(back_button)
        header_layout.add_widget(self.date_label)

        # 스크롤 가능한 내용 영역
        content_layout = BoxLayout(orientation='horizontal', spacing=10)

        # 왼쪽: 일정 및 TODO
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)

        # 일정 섹션
        schedule_label = Label(text='Schedule', font_size='16sp', size_hint_y=None, height='30dp')
        left_layout.add_widget(schedule_label)

        self.schedule_input = TextInput(
            hint_text = 'schedule...',
            multiline = False,
            size_hint_y = None,
            height = '40dp'
        )
        left_layout.add_widget(self.schedule_input)

        add_schedule_btn = Button(
            text = '+',
            size_hint_y = None,
            height = '40dp'
        )
        add_schedule_btn.bind(on_press=self.add_schedule)
        left_layout.add_widget(add_schedule_btn)

        # TODO 섹션
        todo_label = Label(text='TODO List', font_size='16sp', size_hint_y=None, height='30dp')
        left_layout.add_widget(todo_label)

        self.todo_input = TextInput(
            hint_text = 'todo...',
            multiline = False,
            size_hint_y = None,
            height = '40dp'
        )
        left_layout.add_widget(self.todo_input)

        add_todo_btn = Button(
            text = '+',
            size_hint_y = None,
            height = '40dp'
        )
        add_todo_btn.bind(on_press=self.add_todo)
        left_layout.add_widget(add_todo_btn)

        # 저장된 일정/TODO 표시 영역
        self.saved_content = Label(
            text = 'todo',
            text_size = (None, None),
            valign = 'top'
        )
        left_layout.add_widget(self.saved_content)

        # 오른쪽: 이미지 영역
        right_layout = BoxLayout(orientation='vertical', size_hint_x=0.4)

        image_label = Label(text='image', font_size='16sp', size_hint_y=None, height='30dp')
        right_layout.add_widget(image_label)

        self.image_display = Image(
            source='',
            size_hint_y=0.7
        )
        right_layout.add_widget(self.image_display)

        select_image_btn = Button(
            text='+',
            size_hint_y=None,
            height='40dp'
        )
        select_image_btn.bind(on_press=self.select_image)
        right_layout.add_widget(select_image_btn)

        content_layout.add_widget(left_layout)
        content_layout.add_widget(right_layout)

        main_layout.add_widget(header_layout)
        main_layout.add_widget(content_layout)

        self.add_widget(main_layout)


    def load_date(self, date_str):
        self.selected_date = date_str
        # 날짜 형식 변환 (YYYY-MM-DD -> YYYY년 MM월 DD일)
        year, month, day = date_str.split('-')
        self.date_label.text = f'{year}. {month}. {day}.'
        self.load_saved_data()

    def load_saved_data(self):
        if not self.selected_date:
            return
            # 저장된 일정과 TODO 불러오기
        schedules = self.db.get_schedules(self.selected_date)
        todos = self.db.get_todos(self.selected_date)

        content_text = ""

        if schedules:
            content_text += "📅 schedules:\n"
            for schedule in schedules:
                content_text += f"• {schedule[2]} - {schedule[3] or ''}\n"
            content_text += "\n"

        if todos:
            content_text += "✓ TODO:\n"
            for todo in todos:
                status = "✅" if todo[3] else "⬜"
                content_text += f"{status} {todo[2]}\n"

        if not content_text:
            content_text = "no contents."

        self.saved_content.text = content_text
        self.saved_content.text_size = (self.saved_content.width, None)

    def add_schedule(self, instance):
        if not self.selected_date or not self.schedule_input.text:
            return

        self.db.add_schedule(
            self.selected_date,
            self.schedule_input.text,
            self.description_input.text,
            self.selected_image
        )

        # 입력 필드 초기화
        self.schedule_input.text = ''
        self.description_input.text = ''

        # 저장된 데이터 새로고침
        self.load_saved_data()

    def add_todo(self, instance):
        if not self.selected_date or not self.todo_input.text:
            return

        self.db.add_todo(self.selected_date, self.todo_input.text)

        # 입력 필드 초기화
        self.todo_input.text = ''

        # 저장된 데이터 새로고침
        self.load_saved_data()

    def select_image(self, instance):
        # 파일 선택 팝업
        content = BoxLayout(orientation='vertical')

        filechooser = FileChooserListView(
            filters=['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']
        )
        content.add_widget(filechooser)

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')

        select_btn = Button(text='선택')
        cancel_btn = Button(text='취소')

        button_layout.add_widget(select_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)

        popup = Popup(
            title='이미지 파일 선택',
            content=content,
            size_hint=(0.8, 0.8)
        )

        def select_file(instance):
            if filechooser.selection:
                self.selected_image = filechooser.selection[0]
                self.image_display.source = self.selected_image
            popup.dismiss()

        def cancel_selection(instance):
            popup.dismiss()

        select_btn.bind(on_press=select_file)
        cancel_btn.bind(on_press=cancel_selection)

        popup.open()

    def go_back(self, instance):
        # 달력 화면으로 돌아갈 때 달력 새로고침
        calendar_screen = self.manager.get_screen('calendar')
        calendar_screen.build_calendar()
        self.manager.current = 'calendar'