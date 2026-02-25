# ------------------------------------------------------------
# src/data/loader.py
# ------------------------------------------------------------

"""
A tiny, self‑contained loader for the *legal‑rag‑sbert* project.

It walks a directory, reads every ``*.txt`` file and returns a list of
plain‑Python dictionaries that the rest of the pipeline expects:

    {
        "filename":      <str>,   # e.g. "contract_001.txt"
        "content":      <str>,   # the whole file text (empty string if unreadable)
        "source_path":  <str>,   # absolute path on disk
        "source_file":  <str>,   # duplicate of ``filename`` – convenient for later steps
        "file_type":    <str>,   # file extension without the dot, lower‑cased (e.g. "txt")
    }

If a file cannot be read at all, the loader records an **empty string** for
``content`` and logs a warning – the downstream code will then filter it out
before chunking.
"""

import logging
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)

class DocumentLoader:
    """Load plain‑text documents from a directory."""

    def __init__(self, encoding: str = "utf-8"):
        """
        Parameters
        ----------
        encoding: str, optional
            Primary text encoding to try.  If the file cannot be decoded with this
            encoding the loader falls back to a few common alternatives and,
            finally, to ``errors="replace"``.
        """
        self.encoding = encoding

    # ------------------------------------------------------------------
    # Private helper – read a single file, never returns ``None``.
    # ------------------------------------------------------------------
    def _read_file(self, path: Path) -> str:
        """
        Return the whole file as a string.  On any error an empty string is
        returned and a warning is emitted – this guarantees ``len(content)`` is
        always safe to call.
        """
        # 1️⃣ Preferred encoding
        try:
            return path.read_text(encoding=self.encoding)
        except UnicodeDecodeError as e:
            logger.warning(
                f"UnicodeDecodeError reading {path.name} with {self.encoding}: {e}"
            )
        except Exception as e:          # e.g. PermissionError, FileNotFoundError
            logger.warning(f"Cannot read {path.name}: {e}")

        # 2️⃣ Common fall‑backs for legal corpora (Latin‑1, Windows‑1252, UTF‑16)
        for fallback in ("latin-1", "cp1252", "utf-16"):
            try:
                return path.read_text(encoding=fallback)
            except Exception:
                continue

        # 3️⃣ Raw bytes → decode with “replace” (keeps something readable)
        try:
            raw = path.read_bytes()
            return raw.decode(errors="replace")
        except Exception as e:
            logger.error(f"Failed to decode {path.name} even with fallback: {e}")

        # If everything failed we still return a *string* (empty) – never None.
        return ""

    # ------------------------------------------------------------------
    # Public API – walk a directory and produce a list of document dicts.
    # ------------------------------------------------------------------
    def load_all_documents(self, directory: Path) -> List[Dict]:
        """
        Parameters
        ----------
        directory : pathlib.Path
            Folder that contains the ``*.txt`` files to ingest.

        Returns
        -------
        List[dict]
            One dict per file, each containing the keys described in the module
            doc‑string.
        """
        directory = Path(directory)

        if not directory.is_dir():
            raise ValueError(f"'{directory}' is not a valid directory")

        logger.info(f"Scanning {directory} for *.txt files …")
        txt_paths = sorted(directory.glob("*.txt"))

        documents: List[Dict] = []
        for p in txt_paths:
            if not p.is_file():
                logger.debug(f"Skipping non‑file path {p}")
                continue

            # ------------------------------------------------------------
            # 1️⃣ Read the file (never None)
            # ------------------------------------------------------------
            content = self._read_file(p)

            # ------------------------------------------------------------
            # 2️⃣ Derive auxiliary metadata fields that the Preprocessor
            #    expects later on.
            # ------------------------------------------------------------
            filename = p.name
            file_type = p.suffix.lstrip(".").lower()   # e.g. "txt"
            source_file = filename                      # convenient alias

            if content == "":
                logger.warning(
                    f"File {filename} produced empty content after all read attempts"
                )

            documents.append(
                {
                    "filename": filename,
                    "content": content,            # ALWAYS a string (may be "")
                    "source_path": str(p),
                    "source_file": source_file,    # duplicate of filename
                    "file_type": file_type,        # e.g. "txt"
                }
            )

        return documents
# ------------------------------------------------------------
# End of src/data/loader.py
# ------------------------------------------------------------
