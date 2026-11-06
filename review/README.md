# Review marker index

`review_index.json` is the curated list of review notes for this repository.
The nightly reminder job reads it and routes each note to the owner named in
the description.

Every entry has four fields:

| field       | meaning                                                        |
|-------------|----------------------------------------------------------------|
| `id`        | stable audit identifier, used in reminder subjects             |
| `file`      | repository-relative path of the source file                    |
| `line`      | 1-based line number in the current revision of that file       |
| `description` | exact text following the `REVIEW` keyword, owner tag included |

The description is the contract: it is compared verbatim, so do not paraphrase
it or drop the owner tag.  If a note is removed from the source, its entry must
leave the index as well; otherwise the reminder job will keep pinging an owner
about a note that no longer exists.
