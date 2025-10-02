use git2::{Repository, StatusOptions};
use std::env;

fn main() {
    print!("{}", git_prompt());
}

fn git_prompt() -> String {
    let mut result = String::new();

    // Open repository from current directory
    let mut repo = match Repository::discover(".") {
        Ok(repo) => repo,
        Err(_) => return result,
    };

    // Initial space
    result.push(' ');

    // Depth: count how many directories deep we are from repo root
    if let Ok(cwd) = env::current_dir() {
        if let Ok(workdir) = repo.workdir().ok_or("no workdir") {
            if let Ok(rel_path) = cwd.strip_prefix(workdir) {
                let depth = rel_path.components().count();
                for _ in 0..depth {
                    result.push('.');
                }
            }
        }
    }

    // Branch name
    if let Ok(head) = repo.head() {
        if let Some(name) = head.shorthand() {
            result.push_str(name);
        } else if let Ok(oid) = head.target().ok_or("no target") {
            // Detached HEAD - show short hash
            let hash = format!("{}", oid);
            result.push_str(&hash[..7.min(hash.len())]);
        }
    }

    // Is dirty?
    if is_dirty(&repo) {
        result.push('+');
    }

    // Has stashed changes?
    let mut has_stash = false;
    let _ = repo.stash_foreach(|_, _, _| {
        has_stash = true;
        false // stop iterating
    });

    if has_stash {
        result.push('&');
    }

    result
}

fn is_dirty(repo: &Repository) -> bool {
    // Use libgit2 status check for accurate dirty detection
    let mut opts = StatusOptions::new();
    opts.include_untracked(true);
    opts.recurse_untracked_dirs(true);

    if let Ok(statuses) = repo.statuses(Some(&mut opts)) {
        !statuses.is_empty()
    } else {
        false
    }
}
