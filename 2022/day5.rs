use std::fs;

const DAY:&str = "5";

fn main() {
    let filename = format!("day{}.test.input",DAY);
    let contents = fs::read_to_string(filename)
        .expect("Expected to read file");
    println!("== Part 1 ==");
    part1(&contents);
    println!("== Part 2 ==");
    part2(&contents);
}

fn part1(contents: &str) {
    let mut stacks:Vec<Vec<u32>> = Vec::new();
    for i in 0..
    let mut stack_n : u8 = 0;
    let mut i : u32 = 0;
    let mut crates_i : u32 = 0;
    let mut buf : String = String::new();
    let mut read_state : u8 = 0;
    for c in contents.chars() {
        if read_state == 0 || read_state == 1 {
            buf.push_str(&c.to_string());
            crates_i += 1;
            if crates_i == 3 {
                println!("check buf for crate");
                println!("buf: {}",buf);
                if buf == "   " {
                    println!("buf is empty space");
                } else if buf.chars().nth(0).unwrap() == '[' && buf.chars().nth(2).unwrap() == ']' {
                    println!("buf is crate {}",buf.chars().nth(1).unwrap());

                } else if buf.chars().nth(1).unwrap() != ' ' {
                    println!("buf is crate index {}",buf.chars().nth(1).unwrap());
                    read_state = 1;
                }
                stack_n += 1;
            } else if crates_i == 4 {
                if c == '\n' {
                    stack_n = 0;
                    if read_state == 1 {
                        read_state = 2;
                    }
                }
                buf = String::new();
                crates_i = 0;
            }
        }
        i += 1;
    }
}

fn part2(contents: &str) {

}
