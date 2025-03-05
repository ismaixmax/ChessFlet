import flet as ft
import chess

class ChessApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.board = chess.Board()
        self.move_history = []
        self.selected_square = None
        self.legal_moves = []
        self.piece_images = self.load_piece_images()
        self.setup_ui()

    def load_piece_images(self):
        return {
            "P": "https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg",
            "N": "https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg",
            "B": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Chess_blt45.svg",
            "R": "https://upload.wikimedia.org/wikipedia/commons/7/72/Chess_rlt45.svg",
            "Q": "https://upload.wikimedia.org/wikipedia/commons/1/15/Chess_qlt45.svg",
            "K": "https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_klt45.svg",
            "p": "https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg",
            "n": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg",
            "b": "https://upload.wikimedia.org/wikipedia/commons/9/98/Chess_bdt45.svg",
            "r": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg",
            "q": "https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg",
            "k": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg",
        }

    def setup_ui(self):
        self.page.title = "Chess App"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.turn_label = ft.Text(
            value=f"Turn: {'White' if self.board.turn == chess.WHITE else 'Black'}",
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        self.board_grid = ft.GridView(
            expand=True,
            runs_count=8,
            max_extent=self.calculate_tile_size(),
            child_aspect_ratio=1,
        )
        self.update_board()

        self.undo_button = ft.ElevatedButton(text="Undo", on_click=self.on_undo, disabled=True)
        self.redo_button = ft.ElevatedButton(text="Redo", on_click=self.on_redo, disabled=True)
        self.reset_button = ft.ElevatedButton(text="Reset", on_click=self.on_reset)

        self.page.add(
            ft.Column(
                [
                    ft.Row([self.turn_label], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(
                        content=self.board_grid,
                        alignment=ft.alignment.center,
                        width=self.calculate_board_size(),
                        height=self.calculate_board_size(),
                    ),
                    ft.Row(
                        [self.undo_button, self.redo_button, self.reset_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            )
        )

    def calculate_board_size(self):
        screen_width = self.page.width
        screen_height = self.page.height
        board_size = min(screen_width, screen_height) * 0.9  # 90% of the smaller dimension
        max_size = 600  # Matches the window width
        return min(board_size, max_size)

    def calculate_tile_size(self):
        return self.calculate_board_size() // 8

    def update_board(self):
        self.board_grid.controls.clear()
        for rank in range(8):
            for file in range(8):
                square = chess.square(file, 7 - rank)
                piece = self.board.piece_at(square)
                piece_symbol = piece.symbol() if piece else None
                image_url = self.piece_images.get(piece_symbol, None)
                highlight_color = "#F6F669" if square == self.selected_square else ("#ADD8E6" if square in self.legal_moves else None)
                tile = ft.Container(
                    content=ft.Image(src=image_url, width=self.calculate_tile_size() - 20, height=self.calculate_tile_size() - 20) if image_url else None,
                    width=self.calculate_tile_size(),
                    height=self.calculate_tile_size(),
                    bgcolor=highlight_color if highlight_color else ("#DDB88C" if (rank + file) % 2 else "#A66D4F"),
                    alignment=ft.alignment.center,
                    on_click=lambda e, s=square: self.on_square_click(s)
                )
                self.board_grid.controls.append(tile)
        self.page.update()
        def on_square_click(self, square):
            """Handle square click events."""
            if self.selected_square is None:
                piece = self.board.piece_at(square)
                if piece and piece.color == (self.board.turn == chess.WHITE):
                    self.selected_square = square
                    self.legal_moves = [move.to_square for move in self.board.legal_moves if move.from_square == square]
            else:
                move = chess.Move(self.selected_square, square)
                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.move_history.append(move)  # Add move to history
                    self.undo_button.disabled = False  # Enable undo button
                    self.redo_button.disabled = True  # Disable redo button after a new move
                self.selected_square = None
                self.legal_moves = []
            self.update_board()
            self.update_turn_label()

            # Check for game over conditions
            if self.board.is_checkmate():
                print("Checkmate!")
            elif self.board.is_stalemate():
                print("Stalemate!")
            elif self.board.is_insufficient_material():
                print("Draw due to insufficient material!")
            elif self.board.is_game_over():
                print("Game over!")

    def update_turn_label(self):
        """Update the turn label to indicate whose turn it is."""
        self.turn_label.value = f"Turn: {'White' if self.board.turn == chess.WHITE else 'Black'}"
        self.page.update()

    def on_undo(self, e):
        """Undo the last move."""
        if self.board.move_stack:
            move = self.board.pop()
            self.move_history.append(move)  # Add undone move to redo history
            self.redo_button.disabled = False  # Enable redo button
            if not self.board.move_stack:
                self.undo_button.disabled = True  # Disable undo button if no moves left
            self.update_board()
            self.update_turn_label()

    def on_redo(self, e):
        """Redo the last undone move."""
        if self.move_history:
            move = self.move_history.pop()
            self.board.push(move)
            self.undo_button.disabled = False  # Enable undo button
            if not self.move_history:
                self.redo_button.disabled = True  # Disable redo button if no moves left
            self.update_board()
            self.update_turn_label()

    def on_reset(self, e):
        """Reset the board to the initial state."""
        self.board.reset()
        self.move_history.clear()
        self.selected_square = None
        self.legal_moves = []
        self.undo_button.disabled = True
        self.redo_button.disabled = True
        self.update_board()
        self.update_turn_label()
    
def main(page: ft.Page):
    page.window_width = 400
    page.window_height = 1100
    page.update()
    ChessApp(page)

ft.app(target=main)