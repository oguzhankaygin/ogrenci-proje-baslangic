package edu.{{paket}};

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class AppTest {
  @Test
  void ikiSayiyiToplar() {
    assertEquals(5, App.topla(2, 3));
  }
}
