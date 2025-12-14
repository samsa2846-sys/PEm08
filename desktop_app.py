"""
MotionCraft Competition Analyzer - Desktop Application
PyQt6 GUI for competitor analysis
"""
import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QFileDialog,
    QTabWidget, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
import base64
import asyncio
from typing import Optional

# Import backend services
from backend.config import settings
from backend.services.analyzer_service import deepseek_analyzer, yandex_vision_analyzer


class AnalysisWorker(QThread):
    """Worker thread for async analysis"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, analysis_type: str, data: dict):
        super().__init__()
        self.analysis_type = analysis_type
        self.data = data
    
    def run(self):
        """Run analysis in background thread"""
        try:
            if self.analysis_type == "text":
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    deepseek_analyzer.analyze_competitor_text(
                        text=self.data['text'],
                        competitor_name=self.data.get('name')
                    )
                )
                loop.close()
                self.finished.emit(result.dict())
            
            elif self.analysis_type == "image":
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    yandex_vision_analyzer.analyze_image(
                        image_base64=self.data['image_base64']
                    )
                )
                loop.close()
                self.finished.emit(result.dict())
        
        except Exception as e:
            self.error.emit(str(e))


class CompetitionMonitor(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.current_image_path = None
        self.worker = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🎬 MotionCraft Competition Analyzer")
        self.setMinimumSize(900, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("MotionCraft AI Competition Analyzer")
        header.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        subtitle = QLabel("Professional tool for analyzing 3D animation and motion design competitors")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Text Analysis Tab
        self.text_tab = self.create_text_analysis_tab()
        self.tabs.addTab(self.text_tab, "📝 Text Analysis")
        
        # Image Analysis Tab
        self.image_tab = self.create_image_analysis_tab()
        self.tabs.addTab(self.image_tab, "🖼️ Image Analysis")
        
        # Settings Tab
        self.settings_tab = self.create_settings_tab()
        self.tabs.addTab(self.settings_tab, "⚙️ Settings")
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Apply styles
        self.apply_styles()
    
    def create_text_analysis_tab(self) -> QWidget:
        """Create text analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Competitor name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Studio Name (optional):"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Buck, Giant, Tendril")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Text input
        layout.addWidget(QLabel("Competitor Text:"))
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "Paste competitor's text here...\n\n"
            "Example: 'Our studio creates innovative 3D animation for IT startups...'"
        )
        layout.addWidget(self.text_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        analyze_btn = QPushButton("🔍 Analyze Text")
        analyze_btn.clicked.connect(self.analyze_text)
        btn_layout.addWidget(analyze_btn)
        
        example_btn = QPushButton("📋 Load Example")
        example_btn.clicked.connect(self.load_example)
        btn_layout.addWidget(example_btn)
        
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.clicked.connect(self.clear_text)
        btn_layout.addWidget(clear_btn)
        
        layout.addLayout(btn_layout)
        
        # Progress bar
        self.text_progress = QProgressBar()
        self.text_progress.setVisible(False)
        layout.addWidget(self.text_progress)
        
        # Results
        layout.addWidget(QLabel("Analysis Results:"))
        self.text_results = QTextEdit()
        self.text_results.setReadOnly(True)
        layout.addWidget(self.text_results)
        
        return widget
    
    def create_image_analysis_tab(self) -> QWidget:
        """Create image analysis tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Image upload
        upload_layout = QHBoxLayout()
        upload_btn = QPushButton("📁 Select Image")
        upload_btn.clicked.connect(self.select_image)
        upload_layout.addWidget(upload_btn)
        
        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_layout.addWidget(self.image_label)
        upload_layout.addStretch()
        layout.addLayout(upload_layout)
        
        # Image preview
        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setMinimumHeight(200)
        self.image_preview.setStyleSheet("border: 2px dashed #ccc; background: #f9f9f9;")
        layout.addWidget(self.image_preview)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        analyze_img_btn = QPushButton("🔍 Analyze Image")
        analyze_img_btn.clicked.connect(self.analyze_image)
        btn_layout.addWidget(analyze_img_btn)
        
        clear_img_btn = QPushButton("🗑️ Clear")
        clear_img_btn.clicked.connect(self.clear_image)
        btn_layout.addWidget(clear_img_btn)
        
        layout.addLayout(btn_layout)
        
        # Progress bar
        self.image_progress = QProgressBar()
        self.image_progress.setVisible(False)
        layout.addWidget(self.image_progress)
        
        # Results
        layout.addWidget(QLabel("Analysis Results:"))
        self.image_results = QTextEdit()
        self.image_results.setReadOnly(True)
        layout.addWidget(self.image_results)
        
        return widget
    
    def create_settings_tab(self) -> QWidget:
        """Create settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("API Configuration"))
        layout.addWidget(QLabel("Configure API keys in .env file:"))
        
        # API status
        status_text = QTextEdit()
        status_text.setReadOnly(True)
        status_text.setMaximumHeight(200)
        
        status = f"""
✅ DeepSeek API: {'Configured' if settings.deepseek_api_key else '❌ Not configured'}
✅ Yandex Vision API: {'Configured' if settings.yandex_vision_api_key else '❌ Not configured'}

Configuration file: .env

Required variables:
- DEEPSEEK_API_KEY
- DEEPSEEK_API_URL
- YANDEX_VISION_API_KEY
- YANDEX_VISION_FOLDER_ID
- YANDEX_VISION_ENDPOINT
"""
        status_text.setPlainText(status)
        layout.addWidget(status_text)
        
        # About
        layout.addWidget(QLabel("\nAbout:"))
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setMaximumHeight(150)
        about_text.setPlainText(
            "MotionCraft Competition Analyzer v1.0.0\n\n"
            "AI-powered tool for analyzing competitors in 3D animation "
            "and motion design industry.\n\n"
            "Powered by DeepSeek AI and Yandex Vision"
        )
        layout.addWidget(about_text)
        
        layout.addStretch()
        return widget
    
    def analyze_text(self):
        """Analyze competitor text"""
        text = self.text_input.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter text to analyze")
            return
        
        if not settings.deepseek_api_key:
            QMessageBox.critical(self, "Error", "DeepSeek API key not configured")
            return
        
        # Show progress
        self.text_progress.setVisible(True)
        self.text_progress.setRange(0, 0)  # Indeterminate
        self.statusBar().showMessage("Analyzing text...")
        self.text_results.clear()
        
        # Start worker
        data = {
            'text': text,
            'name': self.name_input.text().strip() or None
        }
        self.worker = AnalysisWorker("text", data)
        self.worker.finished.connect(self.on_text_analysis_complete)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.start()
    
    def analyze_image(self):
        """Analyze selected image"""
        if not self.current_image_path:
            QMessageBox.warning(self, "Warning", "Please select an image")
            return
        
        if not settings.yandex_vision_api_key:
            QMessageBox.critical(self, "Error", "Yandex Vision API key not configured")
            return
        
        # Read and encode image
        try:
            with open(self.current_image_path, 'rb') as f:
                image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read image: {e}")
            return
        
        # Show progress
        self.image_progress.setVisible(True)
        self.image_progress.setRange(0, 0)
        self.statusBar().showMessage("Analyzing image...")
        self.image_results.clear()
        
        # Start worker
        data = {'image_base64': image_base64}
        self.worker = AnalysisWorker("image", data)
        self.worker.finished.connect(self.on_image_analysis_complete)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.start()
    
    def on_text_analysis_complete(self, result: dict):
        """Handle text analysis completion"""
        self.text_progress.setVisible(False)
        self.statusBar().showMessage("Analysis complete!")
        
        # Format results
        output = f"""
=== Analysis Results ===

📊 Scores:
  • Design: {result['design_score']}/10
  • Animation: {result['animation_potential']}/10
  • Innovation: {result['innovation_score']}/10
  • Execution: {result['technical_execution']}/10
  • Client Focus: {result['client_focus']}/10

✅ Strengths:
"""
        for strength in result['strengths']:
            output += f"  • {strength}\n"
        
        output += f"\n⚠️ Weaknesses:\n"
        for weakness in result['weaknesses']:
            output += f"  • {weakness}\n"
        
        output += f"\n🎨 Style Analysis:\n{result['style_analysis']}\n"
        
        output += f"\n💡 Recommendations:\n"
        for rec in result['improvement_recommendations']:
            output += f"  • {rec}\n"
        
        output += f"\n📝 Summary:\n{result['summary']}"
        
        self.text_results.setPlainText(output)
    
    def on_image_analysis_complete(self, result: dict):
        """Handle image analysis completion"""
        self.image_progress.setVisible(False)
        self.statusBar().showMessage("Analysis complete!")
        
        # Format results
        output = f"""
=== Image Analysis Results ===

📝 Description:
{result['description']}

📊 Scores:
  • Design: {result['design_score']}/10
  • Animation Potential: {result['animation_potential']}/10
  • Visual Style: {result['visual_style_score']}/10

🎨 Visual Style Analysis:
{result['visual_style_analysis']}

💡 Recommendations:
"""
        for rec in result['recommendations']:
            output += f"  • {rec}\n"
        
        self.image_results.setPlainText(output)
    
    def on_analysis_error(self, error: str):
        """Handle analysis error"""
        self.text_progress.setVisible(False)
        self.image_progress.setVisible(False)
        self.statusBar().showMessage("Analysis failed")
        QMessageBox.critical(self, "Analysis Error", f"Error: {error}")
    
    def select_image(self):
        """Select image file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            self.current_image_path = file_path
            self.image_label.setText(f"Selected: {Path(file_path).name}")
            
            # Show preview
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(
                400, 300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_preview.setPixmap(scaled_pixmap)
    
    def load_example(self):
        """Load example text"""
        example = """Студия MotionCraft — лидер в создании 3D-анимации и моушн-дизайна для технологических компаний.

Наши ключевые услуги:
• Создание анимированных роликов для презентаций продуктов
• Разработка 3D-визуализаций для SaaS-платформ
• Производство рекламных роликов для IT-стартапов
• Создание анимированных инфографик

Технологический стек:
- Cinema 4D + Redshift
- After Effects + Lottie
- Blender для 3D-моделирования
- Figma для пре-продакшн

Наш подход: глубокое погружение в продукт клиента, agile-методология работы,
фокус на передаче сложных технических концепций через простую и красивую анимацию.

Портфолио включает проекты для Yandex, Tinkoff, VK и других технологических гигантов."""
        
        self.text_input.setPlainText(example)
        self.name_input.setText("MotionCraft Studio")
        self.statusBar().showMessage("Example loaded")
    
    def clear_text(self):
        """Clear text inputs"""
        self.text_input.clear()
        self.name_input.clear()
        self.text_results.clear()
        self.statusBar().showMessage("Cleared")
    
    def clear_image(self):
        """Clear image"""
        self.current_image_path = None
        self.image_label.setText("No image selected")
        self.image_preview.clear()
        self.image_results.clear()
        self.statusBar().showMessage("Cleared")
    
    def apply_styles(self):
        """Apply application styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 12px;
            }
            QPushButton {
                padding: 8px 16px;
                font-size: 12px;
                border-radius: 4px;
                background-color: #4CAF50;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTextEdit, QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTabBar::tab {
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 3px solid #4CAF50;
            }
        """)


def main():
    """Main application entry point"""
    # Check API keys
    if not settings.deepseek_api_key:
        print("Warning: DEEPSEEK_API_KEY not configured in .env")
    
    if not settings.yandex_vision_api_key:
        print("Warning: YANDEX_VISION_API_KEY not configured in .env")
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("MotionCraft Competition Analyzer")
    
    # Create and show main window
    window = CompetitionMonitor()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

