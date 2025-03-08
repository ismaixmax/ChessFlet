import flet as ft
import chess
import chess.svg as svg

class ChessApp:
    def __init__(self, page: ft.Page, device_type: str):
        self.page = page
        self.device_type = device_type
        self.board = chess.Board()
        self.move_history = []
        self.selected_square = None
        self.legal_moves = []
        self.piece_images = self.load_piece_images()  # Load piece images once
        self.setup_ui()

    def load_piece_images(self):
        return {
            "P": svg.piece(chess.Piece(chess.PAWN, chess.WHITE)),
            "N": svg.piece(chess.Piece(chess.KNIGHT, chess.WHITE)),
            "B": svg.piece(chess.Piece(chess.BISHOP, chess.WHITE)),
            "R": svg.piece(chess.Piece(chess.ROOK, chess.WHITE)),
            "Q": svg.piece(chess.Piece(chess.QUEEN, chess.WHITE)),
            "K": svg.piece(chess.Piece(chess.KING, chess.WHITE)),
            "p": svg.piece(chess.Piece(chess.PAWN, chess.BLACK)),
            "n": svg.piece(chess.Piece(chess.KNIGHT, chess.BLACK)),
            "b": svg.piece(chess.Piece(chess.BISHOP, chess.BLACK)),
            "r": svg.piece(chess.Piece(chess.ROOK, chess.BLACK)),
            "q": svg.piece(chess.Piece(chess.QUEEN, chess.BLACK)),
            "k": svg.piece(chess.Piece(chess.KING, chess.BLACK)),
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
            spacing=0,
            run_spacing=0,
            controls=[
                ft.Container(
                    content=None,
                    alignment=ft.alignment.center,
                    data=square,
                    on_click=self.on_square_click,
                )
                for square in range(64)  # Ensure 64 elements for the chessboard
            ],
        )

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
                        spacing=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            )
        )

        self.update_board()

    def calculate_board_size(self):
        screen_width = self.page.width
        screen_height = self.page.height
        if self.device_type == "Phone":
            board_size = min(screen_width, screen_height) * 1.5  # 80% of the smaller dimension
        elif self.device_type == "Tablet":
            board_size = min(screen_width, screen_height) * 0.7  # 85% of the smaller dimension
        else:  # Desktop
            board_size = min(screen_width, screen_height) * 2  # 90% of the smaller dimension
        max_size = 500  # Matches the window width
        return min(board_size, max_size)

    def calculate_tile_size(self):
        if self.device_type == "Phone":
            return self.calculate_board_size() / 10
        elif self.device_type == "Tablet":
            return self.calculate_board_size() / 8
        else:  # Desktop
            return self.calculate_board_size() / 8

    def update_board(self):
        """Update the board display."""
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                piece_image = self.piece_images[piece.symbol()]
            else:
                piece_image = None

            square_control = self.board_grid.controls[square]
            row, col = divmod(square, 8)
            tile_color = "#D18B47" if (row + col) % 2 == 0 else "#FFCE9E"  # Dark and light colors

            if square in self.legal_moves:
                tile_color = "#ADD8E6"  # Highlight color for legal moves

            if piece_image:
                square_control.content = ft.AnimatedSwitcher(
                    content=ft.Image(src=piece_image),
                    duration=500,  # Animation duration in milliseconds
                    transition=ft.AnimatedSwitcherTransition.SCALE,
                )
            else:
                square_control.content = ft.AnimatedSwitcher(
                    content=ft.Container(),  # Use an empty container instead of None
                    duration=500,  # Animation duration in milliseconds
                    transition=ft.AnimatedSwitcherTransition.SCALE,
                )
            
            square_control.bgcolor = tile_color
            square_control.update()

        self.page.update()

    def update_turn_label(self):
        """Update the turn label to indicate whose turn it is."""
        self.turn_label.value = f"Turn: {'White' if self.board.turn == chess.WHITE else 'Black'}"
        self.turn_label.update()

    def on_square_click(self, e):
        """Handle square click events."""
        square = e.control.data  # Extract the square index from the event
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
            print("Insufficient material!")
        elif self.board.is_seventyfive_moves():
            print("Draw by seventy-five moves rule!")
        elif self.board.is_fivefold_repetition():
            print("Draw by fivefold repetition!")
        elif self.board.is_variant_draw():
            print("Draw by variant rule!")

    def on_undo(self, e):
        """Undo the last move."""
        if self.move_history:
            self.board.pop()
            self.move_history.pop()
            self.redo_button.disabled = False  # Enable redo button
            if not self.move_history:
                self.undo_button.disabled = True  # Disable undo button if no moves left
            self.update_board()
            self.update_turn_label()

    def on_redo(self, e):
        """Redo the last undone move."""
        if self.move_history:
            move = self.move_history[-1]
            self.board.push(move)
            self.move_history.pop()
            self.undo_button.disabled = False

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

    user_agent = page.client_user_agent
    if "Mobile" in user_agent or "Android" in user_agent:
        device_type = "Phone"
    elif "Tablet" in user_agent:
        device_type = "Tablet"
    else:
        device_type = "Desktop"

    print(f"Running on: {device_type}")

    ChessApp(page, device_type)

ft.app(target=main)
