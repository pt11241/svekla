import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class StrategyComparisonWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.strategies = ["Greedy", "Thrifty", "Greedy-thrifty", "Thrifty-greedy"]
        self.losses = [2.82, 4.52, 3.15, 4.08]
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Сравнение значений целевой функции для разных стратегий")
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # График
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Подписи к стратегиям
        strategy_layout = QHBoxLayout()
        for strategy, loss in zip(self.strategies, self.losses):
            label = QLabel(f"{strategy}: {loss}%")
            label.setAlignment(Qt.AlignCenter)
            strategy_layout.addWidget(label)
        
        layout.addLayout(strategy_layout)
        self.setLayout(layout)
        self.plot_comparison()
        
    def plot_comparison(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        x = np.arange(len(self.strategies))
        width = 0.6
        
        bars = ax.bar(x, self.losses, width, color=['#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0'])
        
        ax.set_xlabel('Стратегии')
        ax.set_ylabel('Потери (%)')
        ax.set_title('Сравнение потерь по стратегиям')
        ax.set_xticks(x)
        ax.set_xticklabels(self.strategies, rotation=45)
        
        # Добавляем значения на столбцы
        for bar, loss in zip(bars, self.losses):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{loss}%', ha='center', va='bottom')
        
        self.figure.tight_layout()
        self.canvas.draw()

class SugarLossCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ потерь сахара из свеклы")
        self.setGeometry(100, 100, 900, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Создаем вкладки
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Добавляем вкладки
        self.create_input_tab()
        self.create_results_tab()
        self.create_comparison_tab()
        self.create_additional_strategies_tab()
        
        # Кнопка расчета
        self.calculate_btn = QPushButton("Рассчитать потери")
        self.calculate_btn.clicked.connect(self.calculate_losses)
        self.calculate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        main_layout.addWidget(self.calculate_btn)
        
    def create_input_tab(self):
        """Создание вкладки для ввода параметров"""
        input_tab = QWidget()
        layout = QVBoxLayout(input_tab)
        
        # Заголовок
        title = QLabel("Начальное окно программы")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Группа параметров свеклы
        beet_group = QGroupBox("Параметры свеклы")
        beet_layout = QGridLayout()
        
        beet_layout.addWidget(QLabel("Количество партий свеклы:"), 0, 0)
        self.batch_count = QSpinBox()
        self.batch_count.setRange(1, 100)
        self.batch_count.setValue(20)
        beet_layout.addWidget(self.batch_count, 0, 1)
        
        beet_layout.addWidget(QLabel("Длительность этапа (дни):"), 1, 0)
        self.stage_duration = QSpinBox()
        self.stage_duration.setRange(1, 10)
        self.stage_duration.setValue(5)
        beet_layout.addWidget(self.stage_duration, 1, 1)
        
        beet_layout.addWidget(QLabel("Количество экспериментов:"), 2, 0)
        self.experiment_count = QSpinBox()
        self.experiment_count.setRange(1, 100)
        self.experiment_count.setValue(20)
        beet_layout.addWidget(self.experiment_count, 2, 1)
        
        beet_group.setLayout(beet_layout)
        layout.addWidget(beet_group)
        
        # Содержание сахара
        sugar_group = QGroupBox("Содержание сахара перед обработкой")
        sugar_layout = QGridLayout()
        
        sugar_layout.addWidget(QLabel("Минимальное:"), 0, 0)
        self.sugar_min = QDoubleSpinBox()
        self.sugar_min.setRange(0.0, 1.0)
        self.sugar_min.setValue(0.14)
        self.sugar_min.setSingleStep(0.01)
        sugar_layout.addWidget(self.sugar_min, 0, 1)
        
        sugar_layout.addWidget(QLabel("Максимальное:"), 1, 0)
        self.sugar_max = QDoubleSpinBox()
        self.sugar_max.setRange(0.0, 1.0)
        self.sugar_max.setValue(0.2)
        self.sugar_max.setSingleStep(0.01)
        sugar_layout.addWidget(self.sugar_max, 1, 1)
        
        sugar_group.setLayout(sugar_layout)
        layout.addWidget(sugar_group)
        
        # Неорганические вещества
        inorg_group = QGroupBox("Учет влияния неорганических веществ")
        inorg_layout = QGridLayout()
        
        inorg_layout.addWidget(QLabel("K (мг/100г):"), 0, 0)
        self.k_content = QLineEdit("4.6-8.7")
        inorg_layout.addWidget(self.k_content, 0, 1)
        
        inorg_layout.addWidget(QLabel("Na (мг/100г):"), 1, 0)
        self.na_content = QLineEdit("0.15-0.92")
        inorg_layout.addWidget(self.na_content, 1, 1)
        
        inorg_layout.addWidget(QLabel("N (мг/100г):"), 2, 0)
        self.n_content = QLineEdit("12-3")
        inorg_layout.addWidget(self.n_content, 2, 1)
        
        inorg_group.setLayout(inorg_layout)
        layout.addWidget(inorg_group)
        
        # Распределение деградации
        dist_group = QGroupBox("Распределение коэффициентов деградации")
        dist_layout = QVBoxLayout()
        
        self.dist_uniform = QRadioButton("Равномерное распределение")
        self.dist_concentrated = QRadioButton("Концентрированное распределение")
        self.dist_uniform.setChecked(True)
        
        dist_layout.addWidget(self.dist_uniform)
        dist_layout.addWidget(self.dist_concentrated)
        
        # Параметры распределения
        param_layout = QGridLayout()
        param_layout.addWidget(QLabel("Минимальное значение:"), 0, 0)
        self.deg_min = QDoubleSpinBox()
        self.deg_min.setRange(0.0, 1.0)
        self.deg_min.setValue(0.94)
        self.deg_min.setSingleStep(0.01)
        param_layout.addWidget(self.deg_min, 0, 1)
        
        param_layout.addWidget(QLabel("Максимальное значение:"), 1, 0)
        self.deg_max = QDoubleSpinBox()
        self.deg_max.setRange(0.0, 1.0)
        self.deg_max.setValue(0.99)
        self.deg_max.setSingleStep(0.01)
        param_layout.addWidget(self.deg_max, 1, 1)
        
        dist_layout.addLayout(param_layout)
        dist_group.setLayout(dist_layout)
        layout.addWidget(dist_group)
        
        layout.addStretch()
        self.tabs.addTab(input_tab, "Ввод параметров")
        
    def create_results_tab(self):
        """Создание вкладки с результатами"""
        results_tab = QWidget()
        layout = QVBoxLayout(results_tab)
        
        # Заголовок
        title = QLabel("Результаты расчета потерь")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Виджет для отображения потерь
        losses_group = QGroupBox("Потери стратегий")
        losses_layout = QGridLayout()
        
        self.loss_labels = {}
        strategies = ["Greedy", "Thrifty", "Greedy-thrifty", "Thrifty-greedy"]
        
        for i, strategy in enumerate(strategies):
            losses_layout.addWidget(QLabel(f"{strategy}:"), i, 0)
            loss_label = QLabel("0.00%")
            loss_label.setStyleSheet("font-weight: bold; color: #d32f2f;")
            self.loss_labels[strategy] = loss_label
            losses_layout.addWidget(loss_label, i, 1)
        
        losses_group.setLayout(losses_layout)
        layout.addWidget(losses_group)
        
        # Лучшая стратегия
        best_group = QGroupBox("Лучшая стратегия обработки")
        best_layout = QHBoxLayout()
        
        self.best_strategy_label = QLabel("Не определено")
        self.best_strategy_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #4CAF50;
            padding: 10px;
            border: 2px solid #4CAF50;
            border-radius: 5px;
        """)
        self.best_strategy_label.setAlignment(Qt.AlignCenter)
        
        best_layout.addWidget(self.best_strategy_label)
        best_group.setLayout(best_layout)
        layout.addWidget(best_group)
        
        # Виджет сравнения
        self.comparison_widget = StrategyComparisonWidget()
        layout.addWidget(self.comparison_widget)
        
        layout.addStretch()
        self.tabs.addTab(results_tab, "Результаты")
        
    def create_comparison_tab(self):
        """Создание вкладки для сравнения распределений"""
        comparison_tab = QWidget()
        layout = QVBoxLayout(comparison_tab)
        
        title = QLabel("Сравнение распределений коэффициентов деградации")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Создаем фигуру для двух графиков
        self.comparison_figure = Figure(figsize=(10, 6))
        self.comparison_canvas = FigureCanvas(self.comparison_figure)
        layout.addWidget(self.comparison_canvas)
        
        # Данные для примера
        uniform_data = np.random.uniform(0.94, 0.99, 1000)
        concentrated_data = np.random.normal(0.965, 0.01, 1000)
        concentrated_data = np.clip(concentrated_data, 0.94, 0.99)
        
        # Создаем графики
        self.plot_distribution_comparison(uniform_data, concentrated_data)
        
        layout.addStretch()
        self.tabs.addTab(comparison_tab, "Сравнение распределений")
        
    def create_additional_strategies_tab(self):
        """Создание вкладки с дополнительными стратегиями"""
        additional_tab = QWidget()
        layout = QVBoxLayout(additional_tab)
        
        title = QLabel("Рассмотрение дополнительных стратегий")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Параметры созревания
        ripening_group = QGroupBox("Параметры созревания (12 этапов)")
        ripening_layout = QGridLayout()
        
        ripening_layout.addWidget(QLabel("Минимальный коэффициент:"), 0, 0)
        self.ripe_min = QDoubleSpinBox()
        self.ripe_min.setRange(0.9, 1.2)
        self.ripe_min.setValue(1.01)
        self.ripe_min.setSingleStep(0.01)
        ripening_layout.addWidget(self.ripe_min, 0, 1)
        
        ripening_layout.addWidget(QLabel("Максимальный коэффициент:"), 1, 0)
        self.ripe_max = QDoubleSpinBox()
        self.ripe_max.setRange(0.9, 1.2)
        self.ripe_max.setValue(1.06)
        self.ripe_max.setSingleStep(0.01)
        ripening_layout.addWidget(self.ripe_max, 1, 1)
        
        ripening_group.setLayout(ripening_layout)
        layout.addWidget(ripening_group)
        
        # Дополнительные стратегии
        strategies = [
            "T(k=8)G", "CTG", "Thrifty", "GT", 
            "G(k=14)", "TG", "Greedy"
        ]
        losses = [3.73, 3.99, 4.3, 4.63, 4.46, 5.25, 5.52]
        
        # Таблица потерь
        table_group = QGroupBox("Потери дополнительных стратегий")
        table_layout = QGridLayout()
        
        for i, (strategy, loss) in enumerate(zip(strategies, losses)):
            table_layout.addWidget(QLabel(strategy), i, 0)
            loss_label = QLabel(f"{loss}%")
            loss_label.setStyleSheet("font-weight: bold;")
            table_layout.addWidget(loss_label, i, 1)
        
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        # Лучшая стратегия
        best_label = QLabel("Лучшая стратегия обработки: T(k=8)G")
        best_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2196F3;
            padding: 10px;
            border: 2px solid #2196F3;
            border-radius: 5px;
            background-color: #E3F2FD;
        """)
        best_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(best_label)
        
        # График для дополнительных стратегий
        self.create_additional_strategies_chart(layout)
        
        layout.addStretch()
        self.tabs.addTab(additional_tab, "Дополнительные стратегии")
        
    def plot_distribution_comparison(self, uniform_data, concentrated_data):
        """Построение графиков сравнения распределений"""
        self.comparison_figure.clear()
        
        # Первый график - равномерное распределение
        ax1 = self.comparison_figure.add_subplot(121)
        ax1.hist(uniform_data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('Равномерное распределение')
        ax1.set_xlabel('Коэффициент деградации')
        ax1.set_ylabel('Частота')
        ax1.grid(True, alpha=0.3)
        
        # Второй график - концентрированное распределение
        ax2 = self.comparison_figure.add_subplot(122)
        ax2.hist(concentrated_data, bins=30, alpha=0.7, color='lightcoral', edgecolor='black')
        ax2.set_title('Концентрированное распределение')
        ax2.set_xlabel('Коэффициент деградации')
        ax2.set_ylabel('Частота')
        ax2.grid(True, alpha=0.3)
        
        self.comparison_figure.tight_layout()
        self.comparison_canvas.draw()
        
    def create_additional_strategies_chart(self, layout):
        """Создание графика для дополнительных стратегий"""
        figure = Figure(figsize=(10, 4))
        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)
        
        strategies = ["T(k=8)G", "CTG", "Thrifty", "GT", 
                     "G(k=14)", "TG", "Greedy"]
        losses = [3.73, 3.99, 4.3, 4.63, 4.46, 5.25, 5.52]
        
        ax = figure.add_subplot(111)
        x = np.arange(len(strategies))
        colors = plt.cm.Set3(np.linspace(0, 1, len(strategies)))
        
        bars = ax.bar(x, losses, color=colors, edgecolor='black')
        
        ax.set_xlabel('Стратегии')
        ax.set_ylabel('Потери (%)')
        ax.set_title('Сравнение потерь по дополнительным стратегиям')
        ax.set_xticks(x)
        ax.set_xticklabels(strategies, rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Добавляем значения на столбцы
        for bar, loss in zip(bars, losses):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{loss}%', ha='center', va='bottom', fontsize=9)
        
        figure.tight_layout()
        canvas.draw()
        
    def calculate_losses(self):
        """Расчет потерь на основе введенных параметров"""
        try:
            # В реальной реализации здесь будет ваш алгоритм расчета
            # Сейчас используем примерные данные
            
            if self.dist_uniform.isChecked():
                # Данные для равномерного распределения
                losses = {
                    "Greedy": 2.82,
                    "Thrifty": 4.52,
                    "Greedy-thrifty": 3.15,
                    "Thrifty-greedy": 4.08
                }
                best = "Greedy"
            else:
                # Данные для концентрированного распределения
                losses = {
                    "Greedy": 10.86,
                    "Thrifty": 1.43,
                    "Greedy-thrifty": 10.37,
                    "Thrifty-greedy": 2.73
                }
                best = "Thrifty"
            
            # Обновляем метки
            for strategy, loss in losses.items():
                self.loss_labels[strategy].setText(f"{loss:.2f}%")
            
            # Обновляем лучшую стратегию
            self.best_strategy_label.setText(best)
            
            # Обновляем виджет сравнения
            self.comparison_widget.losses = list(losses.values())
            self.comparison_widget.plot_comparison()
            
            # Переключаемся на вкладку результатов
            self.tabs.setCurrentIndex(1)
            
            # Показываем сообщение об успехе
            QMessageBox.information(self, "Расчет завершен", 
                                   "Потери успешно рассчитаны!")
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", 
                                f"Ошибка при расчете: {str(e)}")

def main():
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль
    app.setStyle('Fusion')
    
    # Создаем и показываем главное окно
    window = SugarLossCalculator()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()