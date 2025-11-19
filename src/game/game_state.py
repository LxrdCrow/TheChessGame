from typing import Optional, Tuple, List, Dict, Any
from src.game.board import Board
from src.game.rules import Rules
from src.game.constants import TILE_SIZE, BOARD_WIDTH, BOARD_HEIGHT
import pygame as pg

Position = Tuple[int, int]  # (row, col)


class GameState:
    """
    Pure game-state logic for a chess game (UI-agnostic).
    Responsibilities:
      - track current player color ("white" or "black")
      - maintain halfmove/fullmove counters
      - maintain en-passant target square
      - maintain castling rights snapshot (if managed on Board)
      - keep move history with enough metadata to allow undo
    """

    def __init__(self, board: Optional[Board] = None):
        # Board instance will be attached with start_new_game or passed directly
        self.board: Optional[Board] = board

        # Who moves next: "white" or "black"
        self.current_color: str = "white"

        # FEN-like counters
        self.halfmove_clock: int = 0
        self.fullmove_number: int = 1

        # en-passant target square (row, col) or None
        self.en_passant_target: Optional[Position] = None

        # castling rights snapshot (you can store as dict {'white_k': True, ...})
        # It's optional: if your Board tracks castling rights, we'll snapshot it if present.
        self.castling_rights: Optional[Dict[str, bool]] = None

        # history stack: each entry stores metadata to undo the move
        self.move_history: List[Dict[str, Any]] = []

        # reference to captured pieces if you want to display them
        self.captured_pieces: List[Any] = []

        if board:
            self.start_new_game(board)


    def handle_event(self, event: pg.event.Event) -> None:
        """
        UI adapter: left click select/move, 'u' = undo, 'r' = restart.
        """
        # LEFT CLICK: select or attempt move
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if not self.board:
                return

            mx, my = event.pos
            row = my // TILE_SIZE
            col = mx // TILE_SIZE

            if not (0 <= row < BOARD_HEIGHT and 0 <= col < BOARD_WIDTH):
                return

            # If no selection -> try select
            if getattr(self.board, "selected_piece", None) is None:
                self.board.select_piece((row, col))
                return

            # If selection exists -> attempt move
            start_pos = self.board.selected_piece.position
            end_pos = (row, col)
            moved = self.apply_move(start_pos, end_pos)
            if moved:
                # successful: clear selection (and GameState already switched turn)
                self.board.selected_piece = None
            else:
                # if failed, try select piece on clicked square (possibly change selection)
                self.board.select_piece((row, col))
            return

        # KEYBOARD shortcuts
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_u:
                self.undo_last_move()
                return
            if event.key == pg.K_r:
                if self.board:
                    self.board.load_board()
                    self.start_new_game(self.board)
                return
            return

    # -------------------------
    # Initialization / helpers
    # -------------------------
    def start_new_game(self, board: Board):
        """Attach a Board and reset all counters for a new game."""
        self.board = board
        self.current_color = "white"
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.en_passant_target = getattr(board, "en_passant_target", None)
        self.castling_rights = getattr(board, "castling_rights", None)
        self.move_history.clear()
        self.captured_pieces.clear()

    def get_current_player_color(self) -> str:
        return self.current_color

    # -------------------------
    # Apply / record moves
    # -------------------------
    def apply_move(self, start_pos: Position, end_pos: Position) -> bool:
        """
        Apply a move on the attached board.
        This method:
         - validates & executes the move via board.move_piece
         - updates internal clocks and counters
         - pushes a detailed history record for undo
        Returns True if the move was executed.
        """
        if self.board is None:
            raise RuntimeError("No board attached to GameState")

        start_row, start_col = start_pos
        end_row, end_col = end_pos

        moving_piece = self.board.tiles[start_row][start_col]
        if not moving_piece:
            return False  # nothing to move

        # quick turn sanity check
        if moving_piece.color != self.current_color:
            return False

        # Prepare history snapshot
        history_entry: Dict[str, Any] = {
            "start_pos": start_pos,
            "end_pos": end_pos,
            "moved_piece_ref": moving_piece,
            "moved_piece_prev_type": moving_piece.type,
            "moved_piece_prev_has_moved": getattr(moving_piece, "has_moved", False),
            "captured_piece": self.board.tiles[end_row][end_col],
            "prev_en_passant": getattr(self.board, "en_passant_target", None),
            "prev_castling_rights": getattr(self.board, "castling_rights", None),
            "prev_halfmove": self.halfmove_clock,
            "prev_fullmove": self.fullmove_number,
            # placeholders for special-case data
            "castle": None,
            "promotion": None,
        }

        # Detect castling attempt (king moving two columns)
        if moving_piece.type.lower() == "king" and abs(start_col - end_col) == 2:
            history_entry["castle"] = {
                "is_castle": True,
                "king_start": start_pos,
                "king_end": end_pos,
                # rook positions will be filled after move executes (we can compute now)
            }

        # Detect pawn promotion possibility (we'll check after move executes to see if it promoted)
        promotion_possible = moving_piece.type.lower() == "pawn" and (end_row == 0 or end_row == 7)

        # Execute the move using Board's logic (it already calls Rules)
        moved = self.board.move_piece(start_pos, end_pos)
        if not moved:
            return False

        # After execution, capture the actual resulting state (promotions, rook moved in castling, etc.)
        moved_piece = self.board.tiles[end_row][end_col]
        history_entry["moved_piece_ref"] = moved_piece

        # Update captured piece AFTER move: handle en-passant & castling captures
        captured_after = None
        if isinstance(self.board.last_move, dict):
            captured_after = self.board.last_move.get("captured")
        # fallback: if board.last_move isn't dict or doesn't include captured, keep original
        if captured_after is None:
            captured_after = history_entry.get("captured_piece")
        history_entry["captured_piece"] = captured_after

        # If there was a captured piece, store it also in global captured_pieces
        if history_entry["captured_piece"] is not None and history_entry["captured_piece"] not in self.captured_pieces:
            self.captured_pieces.append(history_entry["captured_piece"])

        # If a pawn moved or a capture happened, reset halfmove, else increment
        if history_entry["captured_piece"] is not None or history_entry["moved_piece_prev_type"].lower() == "pawn":
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # fullmove_number increments after Black has moved
        if self.current_color == "black":
            self.fullmove_number += 1

        # Update en-passant target from board (board.update_en_passant should be called inside board.move_piece)
        self.en_passant_target = getattr(self.board, "en_passant_target", None)

        # Update castling rights snapshot (if board keeps them)
        self.castling_rights = getattr(self.board, "castling_rights", None)

        # Promotion detection: if piece type changed after move and it was a pawn before
        if promotion_possible and history_entry["moved_piece_prev_type"].lower() == "pawn":
            if moved_piece.type.lower() != "pawn":
                history_entry["promotion"] = {
                    "promoted_to": moved_piece.type,
                    "prev_type": "pawn"
                }

        # Append to history stack
        self.move_history.append(history_entry)

        # Switch current player
        self._switch_turn()

        return True

    # -------------------------
    # Undo
    # -------------------------
    def undo_last_move(self) -> bool:
        """
        Undo the last applied move. Restores positions and common flags.
        Note: Undo tries to restore:
          - moved piece to start_pos and its previous 'has_moved' and 'type'
          - restore captured piece (if any) at end_pos
          - restore en-passant target and castling rights snapshots
          - restore halfmove and fullmove counters
        """
        if not self.move_history or self.board is None:
            return False

        last = self.move_history.pop()

        start_pos: Position = last["start_pos"]
        end_pos: Position = last["end_pos"]
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        moved_piece = self.board.tiles[end_row][end_col]  # piece currently on end square
        # If the move was castling, the king/rook might have been moved to different squares;
        # we handle king->rook restoration generically below.

        # 1) Remove piece from end square and place it back to start
        self.board.tiles[start_row][start_col] = moved_piece
        self.board.tiles[end_row][end_col] = last["captured_piece"]  # could be None
        if moved_piece:
            moved_piece.position = (start_row, start_col)

        # 2) Restore has_moved flag and type (for promotion undo)
        if moved_piece:
            moved_piece.has_moved = last.get("moved_piece_prev_has_moved", getattr(moved_piece, "has_moved", False))
            prev_type = last.get("moved_piece_prev_type")
            if prev_type:
                moved_piece.type = prev_type

        # 3) If castling occurred, move rook back (best-effort)
        if last.get("castle"):
            # We attempt to detect rook current position and restore it.
            # Assumes that board.move_piece used the convention:
            # - kingside: rook moved to column 5 (index 5), queenside: rook moved to column 3.
            king_start = last["castle"]["king_start"]
            king_end = last["castle"]["king_end"]
            kr, kc = king_start
            er, ec = king_end
            # detect rook final col (where a rook would be after castle)
            if ec > kc:
                # kingside: rook likely at col 5
                rook_new_col = 5
                rook_orig_col = 7
            else:
                # queenside: rook likely at col 3
                rook_new_col = 3
                rook_orig_col = 0

            rook_piece = self.board.tiles[kr][rook_new_col]
            if rook_piece:
                # move rook back
                self.board.tiles[kr][rook_new_col] = None
                self.board.tiles[kr][rook_orig_col] = rook_piece
                rook_piece.position = (kr, rook_orig_col)
                # no reliable previous has_moved stored here; if needed store it in history

        # 4) Restore en-passant target and castling rights and counters
        self.en_passant_target = last.get("prev_en_passant")
        if hasattr(self.board, "en_passant_target"):
            self.board.en_passant_target = self.en_passant_target

        self.castling_rights = last.get("prev_castling_rights")
        if hasattr(self.board, "castling_rights"):
            self.board.castling_rights = self.castling_rights

        self.halfmove_clock = last.get("prev_halfmove", self.halfmove_clock)
        self.fullmove_number = last.get("prev_fullmove", self.fullmove_number)

        # If we restored a captured piece, remove it from captured_pieces stack
        if last.get("captured_piece") is not None and self.captured_pieces:
            # remove last occurrence matching the captured piece (best-effort)
            try:
                self.captured_pieces.remove(last["captured_piece"])
            except ValueError:
                pass

        # Finally, switch turn back
        self._switch_turn(backwards=True)

        return True

    # -------------------------
    # Turn helpers
    # -------------------------
    def _switch_turn(self, backwards: bool = False):
        """Switch current_color; if backwards=True it undoes a switch (used for undo)."""
        if backwards:
            # undoing: previous color becomes current again (flip)
            self.current_color = "white" if self.current_color == "black" else "black"
        else:
            self.current_color = "white" if self.current_color == "black" else "black"

    # -------------------------
    # Check / checkmate stubs
    # -------------------------
    def is_in_check(self, color: str) -> bool:
        """
        Returns True if the king of given color is in check.
        TODO: implement detection using Rules.is_in_check or board scanning.
        """
        # If you implement Rules.is_in_check(board, color), simply call it:
        try:
            return Rules.is_in_check(self.board, color)
        except Exception:
            # fallback: not implemented
            return False

    def is_checkmate(self, color: str) -> bool:
        """
        Returns True if the given color is checkmated.
        TODO: implement by checking is_in_check and no legal moves.
        """
        try:
            return Rules.is_checkmate(self.board, color)
        except Exception:
            return False

    # -------------------------
    # Utilities: history access
    # -------------------------
    def get_move_history(self) -> List[Dict[str, Any]]:
        return self.move_history

    def peek_last_move(self) -> Optional[Dict[str, Any]]:
        return self.move_history[-1] if self.move_history else None

